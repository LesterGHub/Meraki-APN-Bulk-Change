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

<img width="1010" height="674" alt="image" src="https://github.com/user-attachments/assets/5030b4c8-0d77-443c-9dc1-5d3c0e78d726" />



## Disclaimer

Use at your own risk. Test in lab environments before production deployment.



