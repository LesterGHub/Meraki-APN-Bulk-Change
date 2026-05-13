from tkinter import StringVar
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.meraki.com/api/v1"
SETTINGS_FILE = "settings.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MerakiAPNTool(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Meraki MX67C APN Bulk Changer")
        self.geometry("1400x900")

        self.devices = []

        self.create_widgets()
        self.load_settings()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def create_widgets(self):

        # Title
        title = ctk.CTkLabel(
            self,
            text="Meraki MX67C APN Bulk Changer",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=20)

        # -------------------------------------------------
        # Top Frame
        # -------------------------------------------------

        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=10)

        # API Key
        ctk.CTkLabel(
            top_frame,
            text="Meraki API Key"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.api_key_entry = ctk.CTkEntry(
            top_frame,
            width=500,
            show="*"
        )

        self.api_key_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Org ID
        ctk.CTkLabel(
            top_frame,
            text="Organization ID"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.org_id_entry = ctk.CTkEntry(
            top_frame,
            width=500
        )

        self.org_id_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # APN
        ctk.CTkLabel(
            top_frame,
            text="New APN"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.apn_entry = ctk.CTkEntry(
            top_frame,
            width=500
        )

        self.apn_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        # -------------------------------------------------
        # Button Frame
        # -------------------------------------------------

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)

        self.fetch_button = ctk.CTkButton(
            button_frame,
            text="Fetch MX67C Devices",
            command=self.fetch_devices,
            width=220,
            height=40
        )

        self.fetch_button.pack(side="left", padx=10, pady=10)

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Bulk Update APN",
            command=self.bulk_update,
            width=220,
            height=40,
            fg_color="green"
        )

        self.update_button.pack(side="left", padx=10, pady=10)

        self.export_button = ctk.CTkButton(
            button_frame,
            text="Export Results",
            command=self.export_results,
            width=220,
            height=40
        )

        self.export_button.pack(side="left", padx=10, pady=10)

        self.select_all_button = ctk.CTkButton(
            button_frame,
            text="Select All",
            command=self.select_all_devices,
            width=180,
            height=40,
            fg_color="orange"
        )

        self.select_all_button.pack(side="left", padx=10, pady=10)

        # -------------------------------------------------
        # Search Frame
        # -------------------------------------------------

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            search_frame,
            text="Search Device"
        ).pack(side="left", padx=10)

        self.search_var = tk.StringVar()

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            textvariable=self.search_var
        )

        self.search_entry.pack(side="left", padx=10)

        self.search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_devices,
            width=120
        )

        self.search_button.pack(side="left", padx=10)

        self.clear_search_button = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.clear_search,
            width=120
        )

        self.clear_search_button.pack(side="left", padx=10)

        # -------------------------------------------------
        # Table Frame
        # -------------------------------------------------

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "Name",
            "Model",
            "Serial",
            "Network",
            "Status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="extended"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=250)

        self.tree.pack(fill="both", expand=True)

        # -------------------------------------------------
        # Progress Bar
        # -------------------------------------------------

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)

        # -------------------------------------------------
        # Logs
        # -------------------------------------------------

        log_frame = ctk.CTkFrame(self)
        log_frame.pack(fill="both", padx=20, pady=10)

        ctk.CTkLabel(
            log_frame,
            text="Logs"
        ).pack(anchor="w", padx=10, pady=5)

        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=180
        )

        self.log_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # -------------------------------------------------
    # Settings
    # -------------------------------------------------

    def save_settings(self):

        data = {
            "api_key": self.api_key_entry.get(),
            "org_id": self.org_id_entry.get()
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)

    def load_settings(self):

        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)

            self.api_key_entry.insert(
                0,
                data.get("api_key", "")
            )

            self.org_id_entry.insert(
                0,
                data.get("org_id", "")
            )

        except:
            pass

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------

    def log(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.log_text.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

        self.log_text.see("end")

    # -------------------------------------------------
    # Headers
    # -------------------------------------------------

    def get_headers(self):

        return {
            "X-Cisco-Meraki-API-Key": self.api_key_entry.get().strip(),
            "Content-Type": "application/json"
        }

    # -------------------------------------------------
    # Fetch Devices
    # -------------------------------------------------

    def fetch_devices(self):

        self.tree.delete(*self.tree.get_children())
        self.devices.clear()

        self.save_settings()

        org_id = self.org_id_entry.get().strip()

        if not org_id:
            messagebox.showerror(
                "Error",
                "Organization ID required"
            )
            return

        self.log("Fetching devices from organization...")

        try:

            url = f"{BASE_URL}/organizations/{org_id}/devices"

            response = requests.get(
                url,
                headers=self.get_headers()
            )

            response.raise_for_status()

            devices = response.json()

            count = 0

            for device in devices:

                model = str(
                    device.get("model", "")
                ).upper()

                if model.startswith("MX67C"):

                    count += 1

                    self.devices.append(device)

                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            device.get("name"),
                            device.get("model"),
                            device.get("serial"),
                            device.get("networkId"),
                            "Ready"
                        )
                    )

            self.log(f"Loaded {count} MX67C devices")

        except Exception as e:

            messagebox.showerror("Error", str(e))
            self.log(f"ERROR: {e}")

    # -------------------------------------------------
    # Update APN
    # -------------------------------------------------


    def update_apn(self, serial, apn):

        url = f"{BASE_URL}/devices/{serial}/cellular/sims"

        payload = {
            "sims": [
                {
                    "slot": "sim1",
                    "isPrimary": True,
                    "apns": [
                        {
                            "name": apn,
                            "allowedIpTypes": [
                                "ipv4",
                                "ipv6"
                            ],
                            "authentication": {
                                "type": "none"
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.put(
            url,
            headers=self.get_headers(),
            json=payload
        )

        return response




    # -------------------------------------------------
    # Bulk Update
    # -------------------------------------------------

    def bulk_update(self):

        apn = self.apn_entry.get().strip()

        if not apn:
            messagebox.showerror(
                "Error",
                "Please enter APN"
            )
            return

        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "Warning",
                "Please select devices"
            )
            return

        self.progress.set(0)

        total = len(selected_items)

        self.log(f"Starting APN update to: {apn}")

        for index, item in enumerate(selected_items, start=1):

            values = self.tree.item(item, "values")

            name = values[0]
            serial = values[2]

            self.log(f"Updating {name} ({serial})...")

            try:

                response = self.update_apn(
                    serial,
                    apn
                )

                if response.status_code in [200, 201]:

                    self.log(f"SUCCESS: {name}")

                    self.tree.item(
                        item,
                        values=(
                            values[0],
                            values[1],
                            values[2],
                            values[3],
                            "Updated"
                        )
                    )

                else:

                    self.log(
                        f"FAILED: {name} -> {response.text}"
                    )

            except Exception as e:

                self.log(f"ERROR: {name} -> {e}")

            progress_value = index / total

            self.progress.set(progress_value)

            self.update_idletasks()

        self.progress.set(1)

        messagebox.showinfo(
            "Completed",
            "Bulk APN update completed"
        )

    # -------------------------------------------------
    # Search Devices
    # -------------------------------------------------

    def search_devices(self):

        keyword = self.search_var.get().strip().lower()

        self.tree.selection_remove(
            *self.tree.selection()
        )

        for item in self.tree.get_children():

            values = self.tree.item(item, "values")

            name = str(values[0]).lower()
            serial = str(values[2]).lower()

            if keyword in name or keyword in serial:
                self.tree.selection_add(item)

    # -------------------------------------------------
    # Clear Search
    # -------------------------------------------------

    def clear_search(self):

        self.search_var.set("")

        self.tree.selection_remove(
            *self.tree.selection()
        )

    # -------------------------------------------------
    # Select All
    # -------------------------------------------------

    def select_all_devices(self):

        for item in self.tree.get_children():
            self.tree.selection_add(item)

        self.log("All devices selected")

    # -------------------------------------------------
    # Export Results
    # -------------------------------------------------

    def export_results(self):

        data = []

        for item in self.tree.get_children():
            data.append(
                self.tree.item(item)["values"]
            )

        if not data:

            messagebox.showwarning(
                "Warning",
                "No data to export"
            )

            return

        df = pd.DataFrame(
            data,
            columns=[
                "Name",
                "Model",
                "Serial",
                "Network",
                "Status"
            ]
        )

        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel Files", "*.xlsx")
            ]
        )

        if filename:

            df.to_excel(filename, index=False)

            self.log(f"Exported results to {filename}")

            messagebox.showinfo(
                "Export",
                "Export completed"
            )


if __name__ == "__main__":

    app = MerakiAPNTool()

    app.mainloop()