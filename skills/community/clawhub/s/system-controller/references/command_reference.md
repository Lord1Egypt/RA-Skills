# Windows System Controller - Command Reference

## Script Locations

All scripts are located at: `~/.workbuddy/skills/system-controller/scripts/`

---

## 1. window_manager.py - Window Management

### List all visible windows
```
python window_manager.py list
```
Returns JSON array of windows with PID, title, and process name.

### Activate (bring to foreground)
```
python window_manager.py activate --title "Notepad"
python window_manager.py activate --pid 1234
```

### Close a window
```
python window_manager.py close --title "Untitled - Notepad"
python window_manager.py close --pid 1234
```

### Minimize / Maximize
```
python window_manager.py minimize --title "Chrome"
python window_manager.py maximize --pid 1234
```

### Resize and move
```
python window_manager.py resize --pid 1234 --x 100 --y 100 --width 800 --height 600
```

### Send keystrokes (SendKeys format)
```
python window_manager.py send-keys --title "Notepad" --text "Hello World"
```
SendKeys special keys: `{ENTER}`, `{TAB}`, `{ESC}`, `{F1}`, `^(c)` for Ctrl+C, `%(f)` for Alt+F

---

## 2. process_manager.py - Process Management

### List all processes
```
python process_manager.py list
python process_manager.py list --name chrome
```

### Kill a process
```
python process_manager.py kill --name notepad
python process_manager.py kill --pid 1234
python process_manager.py kill --name chrome --force
```

### Start a process
```
python process_manager.py start "notepad.exe"
python process_manager.py start "code" --dir "C:\Projects"
```

### Get process details
```
python process_manager.py info --pid 1234
```

### System resource overview
```
python process_manager.py system
```

---

## 3. hardware_controller.py - Hardware Control

### Volume
```
python hardware_controller.py volume get
python hardware_controller.py volume set --level 75
python hardware_controller.py volume mute
```
Note: Precise volume control requires NirCmd (nircmd.com)

### Screen brightness
```
python hardware_controller.py screen brightness
python hardware_controller.py screen brightness --level 50
```
Works on laptop screens and DDC/CI-enabled monitors.

### Display info
```
python hardware_controller.py screen info
```

### Power management
```
python hardware_controller.py power lock
python hardware_controller.py power sleep
python hardware_controller.py power hibernate
python hardware_controller.py power shutdown --delay 30
python hardware_controller.py power restart --delay 30
python hardware_controller.py power cancel
```

### Network
```
python hardware_controller.py network adapters
python hardware_controller.py network enable --name "Wi-Fi"
python hardware_controller.py network disable --name "Ethernet"
python hardware_controller.py network wifi
python hardware_controller.py network info
```

### USB devices
```
python hardware_controller.py usb list
```

---

## 4. serial_comm.py - Serial Communication

### List serial ports
```
python serial_comm.py list
```

### Auto-detect baud rate
```
python serial_comm.py detect --port COM3
```

### Send data
```
python serial_comm.py send --port COM3 --data "LED_ON" --baud 9600
```

### Receive data
```
python serial_comm.py receive --port COM3 --baud 9600 --timeout 5
```

### Send and wait for response
```
python serial_comm.py chat --port COM3 --data "GET_TEMP" --baud 9600
```

### Monitor mode (real-time)
```
python serial_comm.py monitor --port COM3 --baud 9600 --duration 30
```

Dependencies: `pip install pyserial` (auto-installed on first use)

---

## 5. iot_controller.py - IoT / Smart Home

### Home Assistant
```
# List all entities
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN list

# Get entity state
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN state --entity-id light.living_room

# Turn on/off/toggle
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN on --entity-id light.living_room
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN off --entity-id light.living_room
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN toggle --entity-id switch.fan

# Call any service with parameters
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN on --entity-id light.living_room --data '{"brightness_pct": 50, "color_temp": 350}'

# Call arbitrary service
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN call --domain climate --service set_temperature --entity-id climate.bedroom --data '{"temperature": 24}'
```

### Generic HTTP/REST
```
# GET request
python iot_controller.py http --url http://192.168.1.50:8080 get --path /api/status
python iot_controller.py http --url http://192.168.1.50:8080 get --path /api/data --header "Authorization: Bearer TOKEN"

# POST request
python iot_controller.py http --url http://192.168.1.50:8080 post --path /api/command --body '{"action":"on"}'

# PUT request
python iot_controller.py http --url http://192.168.1.50:8080 put --path /api/config --body '{"name":"updated"}'
```

### Mijia / XiaoMi
```
python iot_controller.py mijia discover
```
Requires: `pip install miio` (manual installation)

Dependencies: `pip install requests` (auto-installed on first use)

---

## Common Patterns

### Arduino LED Control
1. Connect Arduino via USB
2. List ports: `python serial_comm.py list`
3. Send command: `python serial_comm.py send --port COM3 --data "LED_ON" --baud 9600`
4. Read sensor: `python serial_comm.py chat --port COM3 --data "READ_TEMP" --baud 9600`

### Smart Home Automation
1. List lights: `python iot_controller.py homeassistant --url ... --token ... list`
2. Turn on: `python iot_controller.py homeassistant --url ... --token ... on --entity-id light.bedroom`
3. Set brightness: `python iot_controller.py homeassistant --url ... --token ... on --entity-id light.bedroom --data '{"brightness_pct":30}'`

### Application Automation
1. Find window: `python window_manager.py list`
2. Activate: `python window_manager.py activate --title "Excel"`
3. Send input: `python window_manager.py send-keys --title "Excel" --text "^(s)"`  (Ctrl+S)
4. Close: `python window_manager.py close --title "Excel"`
