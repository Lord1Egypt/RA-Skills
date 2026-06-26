```markdown
# 🌊 S2 Spectrum: Edge Hardware Setup Guide / 边缘硬件部署指南

## 1. GPIO Fast-Trigger Wiring (引脚直读接线)
For instant zero-latency smart home triggers (R24AVD1):
* **Pin 5 (S1 - Presence)**: Connect to Raspberry Pi GPIO 17. (High = Occupied).
* **Pin 6 (S2 - Motion)**: Connect to Raspberry Pi GPIO 27. (High = Active).

## 2. Advanced UART Wiring (高级串口接线)
To utilize the `uart` mode for quantized vital signs:
* **TX Pin (Radar)** -> **RX Pin (Raspberry Pi/USB TTL)**
* **RX Pin (Radar)** -> **TX Pin (Raspberry Pi/USB TTL)**
* **Baud Rate**: 115200

**Software Dependencies:**
The radar Python client only requires the serial library:
```bash
pip install pyserial

Security Configuration:
Before the Agent can run the script, the system owner MUST set the environment variable. Add this to your ~/.bashrc or systemd service file:
Bash

export S2_PRIVACY_CONSENT=1