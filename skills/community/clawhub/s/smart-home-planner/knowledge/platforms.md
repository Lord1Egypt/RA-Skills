# Platform Knowledge Base

## Home Assistant

**Type:** Open-source, self-hosted
**Config:** YAML + UI (since 2023.7+ most things configurable via UI)
**Automation syntax:** triggers / conditions / actions
**API:** REST API + WebSocket
**Auth:** Long-lived access tokens (Settings → Long-Lived Access Tokens)
**Server required:** Yes (Raspberry Pi, NAS, PC, or HA Cloud)
**Best for:** Geeks, advanced users, multi-platform integration

### Key Details
- Integrations: 2000+ official + custom integrations
- Zigbee: Via ZHA integration or Zigbee2MQTT (USB coordinator required)
- Matter: Native support since 2023
- Voice: Assist (local), Google Home, Alexa via Nabu Casa or manual setup
- Remote access: Nabu Casa ($6.50/mo) or reverse proxy (free)
- Backup: Google Drive, Samba, local snapshots

### Automation Example
```yaml
automation:
  - alias: "Home Mode"
    trigger:
      - platform: state
        entity_id: device_tracker.phone
        to: "home"
    condition:
      - condition: state
        entity_id: sun.sun
        state: "below_horizon"
    action:
      - service: light.turn_on
        target:
          area_id: hallway
      - service: climate.set_temperature
        target:
          entity_id: climate.living_room
        data:
          temperature: 24
```

### Pros/Cons
| Pros | Cons |
|------|------|
| Most flexible, 2000+ integrations | Requires server hardware |
| Local control, privacy-focused | Steeper learning curve |
| Active community, frequent updates | YAML can be intimidating |
| Works with almost any device | Setup takes time |

---

## 米家/小米

**Type:** Commercial ecosystem, cloud-based
**Config:** Mi Home App (iOS/Android)
**Automation:** App-based scene builder (if-then)
**API:** Cloud API via mijia-api (community), limited official API
**Auth:** QR code scan with Mi Home app
**Server required:** No
**Best for:** Beginners, budget-conscious, pure Xiaomi ecosystem

### Key Details
- Ecosystem: 500+ device types from 300+ partners
- Protocol: BLE Mesh, Zigbee 3.0, WiFi, proprietary
- Hub: Xiaomi Multimode Gateway (Zigbee + BLE + WiFi)
- Voice: XiaoAi speaker (built-in)
- Remote: Via Mi Home app (always cloud-based)
- Sub-devices: Connect via gateway, not directly to WiFi

### Automation via App
```
Mi Home App → Smart → Add Scene
  Trigger: When [device] [condition]
  Action: Then [device] [action]
  Example: When door opens → Turn on hallway light
```

### Automation via mijia-api (Advanced)
```python
from mijiaAPI import mijiaAPI, mijiaDevice

api = mijiaAPI()
api.login()  # QR code scan once

# Get all devices
devices = api.get_devices_list()

# Control device
lamp = mijiaDevice(api, dev_name="Bedroom Lamp")
lamp.on = True
lamp.brightness = 80

# Run scene
scenes = api.get_scenes_list()
api.run_scene(scene_id="xxx", home_id="yyy")
```

### Pros/Cons
| Pros | Cons |
|------|------|
| Cheapest devices, wide ecosystem | Cloud-dependent (privacy concern) |
| Easy setup via app | Limited cross-brand compatibility |
| XiaoAi voice built-in | Automation limited to app capabilities |
| No server needed | API access is unofficial |

---

## Apple HomeKit

**Type:** Commercial ecosystem, local-first
**Config:** Home App (iOS/macOS)
**Automation:** Home App scenes and automations
**API:** HomeKit Accessory Protocol (HAP)
**Auth:** Pairing code (8-digit on device/packaging)
**Server required:** No (HomePod/Apple TV as hub)
**Best for:** Apple ecosystem users, privacy-focused

### Key Details
- Hub: HomePod, HomePod Mini, or Apple TV (always-on)
- Protocol: HAP over WiFi/BLE, Matter support since iOS 16
- Devices: Fewer certified devices, generally more expensive
- Bridge: HomeBridge (community) or HA HomeKit integration for non-HomeKit devices
- Remote: Via iCloud (encrypted end-to-end)
- Voice: Siri

### Automation Example (Home App)
```
Home App → Automation → Create
  When: Someone arrives home
  Accessories: Turn on lights, set thermostat
  Condition: At night
```

### Bridge via Home Assistant
```
HA → Settings → Integrations → HomeKit Bridge
  → Select entities to expose
  → Pair with Home App
  → HA devices appear as HomeKit devices
```

### Programmatic Control via homebridge-mcp-server

MCP server for Homebridge — cross-platform, no re-pairing needed.

```
Agent → MCP (stdio) → homebridge-mcp-server → Homebridge REST API → HomeKit accessories
```

```bash
# Install Homebridge (Docker)
docker run -d --name homebridge --net=host \
  -e HOMEBRIDGE_CONFIG_UI=1 -e HOMEBRIDGE_CONFIG_UI_PORT=8581 \
  -v ~/homebridge:/homebridge homebridge/homebridge:latest

# Install MCP server
npm install -g @mp-consulting/homebridge-mcp-server

# Configure (env vars)
export HOMEBRIDGE_URL="http://localhost:8581"
export HOMEBRIDGE_USERNAME="admin"
export HOMEBRIDGE_PASSWORD="your-password"
```

**MCP Tools:** `list_accessories`, `get_accessory`, `set_accessory`, `get_accessory_layout`, `get_homebridge_status`, `restart_homebridge`, `list_plugins`, `search_plugins`, `get_config`, `update_config`, etc.

**Plugins for non-HomeKit devices:** Xiaomi (`homebridge-mi-smart-home`), Tuya (`homebridge-tuya`), Sonoff (`homebridge-ewelink`), Govee (`homebridge-govee`), etc.

See `knowledge/homekit-guide.md` for full setup guide.

### Pros/Cons
| Pros | Cons |
|------|------|
| Best Apple integration | Fewer device options |
| Local control, strong privacy | Devices generally more expensive |
| End-to-end encryption | Automation less flexible |
| Simple UI, reliable | No Android support |

---

## Cross-Platform Comparison Matrix

| Feature | Home Assistant | 米家/小米 | Apple HomeKit |
|---------|---------------|----------|---------------|
| Cost | Low (open-source) | Low (cheap devices) | High (premium devices) |
| Privacy | ★★★★★ Local | ★★☆☆☆ Cloud | ★★★★☆ E2E encrypted |
| Flexibility | ★★★★★ | ★★★☆☆ | ★★★☆☆ |
| Ease of use | ★★★☆☆ | ★★★★★ | ★★★★☆ |
| Device variety | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Server needed | Yes | No | No (hub device) |
| Offline capable | Yes | No | Partial |
| Voice assistant | Multiple | XiaoAi | Siri |
| Remote access | Manual/Nabu Casa | Built-in | Built-in via iCloud |

## Protocol Reference

| Protocol | Range | Power | Speed | Mesh | Used by |
|----------|-------|-------|-------|------|---------|
| Zigbee | 10-30m | Low | 250kbps | Yes | Aqara, Xiaomi, Hue |
| BLE Mesh | 10-30m | Very low | 1Mbps | Yes | Xiaomi, Yeelight |
| WiFi | 30-50m | High | 100Mbps+ | No | Most IP cameras, some bulbs |
| Matter | 30-50m | Varies | Varies | Thread | Cross-platform standard |
| Z-Wave | 30-100m | Low | 100kbps | Yes | Some HA devices |
