# Meraki-APN-Bulk-Change

Windows GUI tool for bulk updating APN settings on Cisco Meraki MX67C appliances.

## Features

- Bulk APN updates
- Device search
- Select all devices
- Progress bar
- Export results to Excel
- Windows Executable file

## Requirements

- Cisco Meraki Dashboard API enabled
- API Key with organization write access
- Python 3.11+ recommended

## Install via powershell
pip install -r requirements.txt

## Run
python meraki_apn_gui.py

## Build EXE
pyinstaller --onefile --windowed meraki_apn_gui.py

## API Endpoint Used

/devices/{serial}/cellular/sims


## Screenshot

<img width="1053" height="706" alt="image" src="https://github.com/user-attachments/assets/9a1e3bd4-0451-404f-91e5-6d628d501f2a" />


## Disclaimer

Use at your own risk. Test in lab environments before production deployment.



