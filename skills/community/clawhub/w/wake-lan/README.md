# wake-on-lan 🖥️

Wake-on-LAN skill for OpenClaw / AI agents. Send magic packets to wake sleeping/suspended devices on your local network.

## Features

- Wake devices by alias or MAC address
- Dual-method sending: `wakeonlan` CLI + raw UDP sockets (for Termux/Android compatibility)
- Manage saved device aliases (add/remove/list)
- No pre-configured devices — add yours securely

## Installation

```bash
clawhub install wake-on-lan
```

## Usage

```bash
# Add a device (first time)
python3 <skill_dir>/scripts/wol.py add desktop --mac aa:bb:cc:dd:ee:ff --ip 192.168.1.100

# Wake by alias
python3 <skill_dir>/scripts/wol.py desktop

# Wake by MAC directly
python3 <skill_dir>/scripts/wol.py --mac aa:bb:cc:dd:ee:ff --ip 192.168.1.100

# List devices
python3 <skill_dir>/scripts/wol.py list
```

## Requirements

- Python 3.8+
- `wakeonlan` package: `pip install wakeonlan`

## License

MIT
