# Mijia Control Examples

## Setup

```python
from mijiaAPI import mijiaAPI, mijiaDevice

api = mijiaAPI()
api.login()  # QR code scan, one-time
```

## Device Discovery

```python
# List all homes
homes = api.get_homes_list()
for home in homes:
    print(f"Home: {home['name']}, ID: {home['id']}")

# List all devices
devices = api.get_devices_list()
for d in devices:
    print(f"{d['name']} ({d['model']}) - DID: {d['did']}")
```

## Light Control

```python
# Turn on/off
lamp = mijiaDevice(api, dev_name="卧室灯")
lamp.on = True
lamp.on = False

# Adjust brightness (0-100)
lamp.brightness = 80

# Adjust color temperature (warm to cool)
lamp.color_temperature = 4000  # Kelvin

# Toggle
lamp.run_action('toggle')
```

## Curtain Control

```python
curtain = mijiaDevice(api, dev_name="客厅窗帘")
curtain.on = True    # Open
curtain.on = False   # Close

# Set position (0-100%)
curtain.position = 50  # Half open
```

## AC Control

```python
ac = mijiaDevice(api, dev_name="客厅空调")
ac.on = True
ac.target_temperature = 24
ac.mode = 2  # 1=cool, 2=heat, 3=auto, 4=dry, 5=fan
ac.fan_level = 2  # Fan speed
```

## Scene Management

```python
# List all scenes
scenes = api.get_scenes_list()
for s in scenes:
    print(f"Scene: {s['name']}, ID: {s['scene_id']}")

# Run a scene
api.run_scene(scene_id="xxx", home_id="yyy")
```

## Natural Language (via XiaoAi)

```python
api.run("打开卧室灯")
api.run("把空调调到24度")
api.run("打开客厅窗帘")
api.run("晚安")  # Triggers goodnight scene
```

## Batch Operations

```python
# Control multiple lights at once
devices = api.get_devices_list()
lights = [d for d in devices if 'light' in d['model']]

# Batch turn on
data = [
    {"did": d['did'], "siid": 2, "piid": 1, "value": True}
    for d in lights
]
api.set_devices_prop(data)
```

## Monitoring

```python
# Check device status
device_info = api.get_devices_prop([
    {"did": "xxx", "siid": 2, "piid": 1},  # on/off
    {"did": "xxx", "siid": 2, "piid": 3},  # brightness
])

# Get power consumption stats
stats = api.get_statistics({"did": "xxx", "type": "power"})

# Check consumables (filters, batteries)
consumables = api.get_consumable_items()
```

## Complete Home Automation Example

```python
from mijiaAPI import mijiaAPI, mijiaDevice
from datetime import datetime

api = mijiaAPI()

# Ensure logged in
if not api.available:
    api.login()

# Home Mode
def home_mode():
    hour = datetime.now().hour
    lamp = mijiaDevice(api, dev_name="玄关灯")
    lamp.on = True

    if 6 <= hour <= 18:  # Daytime
        curtain = mijiaDevice(api, dev_name="客厅窗帘")
        curtain.on = True

    ac = mijiaDevice(api, dev_name="客厅空调")
    ac.on = True
    ac.target_temperature = 24

# Away Mode
def away_mode():
    devices = api.get_devices_list()
    lights = [d for d in devices if 'light' in d['model']]
    data = [
        {"did": d['did'], "siid": 2, "piid": 1, "value": False}
        for d in lights
    ]
    api.set_devices_prop(data)

    # Run vacuum scene
    scenes = api.get_scenes_list()
    for s in scenes:
        if '扫地' in s['name'] or 'vacuum' in s['name'].lower():
            api.run_scene(s['scene_id'], s['home_id'])
            break

# Sleep Mode
def sleep_mode():
    # Living room off
    living_light = mijiaDevice(api, dev_name="客厅灯")
    living_light.on = False

    # Bedroom dim
    bedroom_light = mijiaDevice(api, dev_name="卧室灯")
    bedroom_light.on = True
    bedroom_light.brightness = 10

    # Curtains close
    curtain = mijiaDevice(api, dev_name="客厅窗帘")
    curtain.on = False

    # Lock door
    lock = mijiaDevice(api, dev_name="门锁")
    lock.run_action('lock')
```
