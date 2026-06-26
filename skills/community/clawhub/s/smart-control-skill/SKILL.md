---
name: mxchip-smart-control
description: "Control smart home devices configured in Smart Plus APP. Use when you need to: (1) Query devices and scenes (lights, AC, switches), (2) Control device power (turn on/off), (3) Control air conditioner (temperature, mode), (4) Trigger smart scenes. Requires MXCHIP_OAUTH_TOKEN environment variable."
---

# Mxchip Smart Control

Control smart home devices configured in Smart Plus APP (智家精灵) through MXCHIP MCP service.

**Developer:** Shanghai MXCHIP Information Technology Co., Ltd. (上海庆科信息有限公司)  
**Official Website:** https://www.mxchip.com/  
**GitHub:** https://github.com/mxchip  
**Support:** https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth

## Overview

This skill provides AI agents with complete control over smart home devices configured in **Smart Plus** (智家精灵) APP using the MCP (Model Context Protocol). Supports device management, air conditioner control, and scene automation through JSON-RPC 2.0 over HTTP.

**Protocol:** MCP with JSON-RPC 2.0  
**Transport:** HTTP  
**Target Application:** Smart Plus APP (智家精灵)

## About MXCHIP

**Shanghai MXCHIP Information Technology Co., Ltd.** (上海庆科信息有限公司) is a leading IoT solution provider in China, specializing in:
- Smart home device connectivity
- IoT cloud platform services
- AI-powered home automation
- MCP (Model Context Protocol) integration

**Smart Plus** (智家精灵) is MXCHIP's official smart home application that allows users to:
- Configure and manage smart devices
- Create automation scenes
- Control devices remotely
- Integrate with AI assistants

## Environment Setup

**Install dependencies:**
```bash
pip install requests
```

**Set OAuth token:**
```bash
export MXCHIP_OAUTH_TOKEN="oauth2_YOUR_TOKEN_HERE"
```

**Get your token:**
1. Visit: https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth
2. Enter your Smart Plus APP account credentials
3. Copy the OAuth2 access token

## Quick Start

### Query Devices and Scenes
```python
from mxchip_mcp_client import MxchipMCPClient

client = MxchipMCPClient()

# List all devices and scenes
result = client.list_home_devices_and_scenes()

# Access devices
for device in result.get('devices', []):
    print(f"{device['name']}: {device['category']}")

# Access scenes
for scene in result.get('scenes', []):
    print(f"{scene['name']}: {scene['scene_id']}")
```

### Control Devices
```python
# Turn on light
client.control_device("device_001", "TurnOnRequest")

# Turn off switch
client.control_device("device_002", "TurnOffRequest")
```

### Control Air Conditioner
```python
# Set temperature to 26°C
client.control_air_conditioner(
    "ac_device_id",
    "SetTemperatureRequest",
    temperature=26
)

# Increase temperature by 2°C
client.control_air_conditioner(
    "ac_device_id",
    "IncrementTemperatureRequest",
    delta="2"
)

# Set cooling mode
client.control_air_conditioner(
    "ac_device_id",
    "SetModeRequest",
    mode="COOL"
)
```

### Trigger Scenes
```python
# Trigger "Coming Home" scene
client.trigger_scene("sceneid_coming_home")
```

## MCP Tools Reference

### 1. list_home_devices_and_scenes

**Description:** Get all smart devices and scenes in your home.

**Parameters:** None

**Returns:**
- `devices`: Array of device objects
  - `device_id`: Device unique identifier
  - `name`: Device name
  - `category`: Device type (LIGHT, AIR_CONDITION, SWITCH, etc.)
  - `status`: Current device status
- `scenes`: Array of scene objects
  - `scene_id`: Scene identifier (format: sceneid_xxx)
  - `name`: Scene name (e.g., "Coming Home", "Sleep Mode")

**Example:**
```python
result = client.list_home_devices_and_scenes()
devices = result.get('devices', [])
scenes = result.get('scenes', [])
```

---

### 2. control_device

**Description:** Control device power state (on/off).

**Parameters:**
- `device_id` (string, required): Device identifier from list_home_devices_and_scenes
- `action` (string, required): Control action
  - `"TurnOnRequest"`: Turn on device
  - `"TurnOffRequest"`: Turn off device

**Example:**
```python
# Turn on device
client.control_device("light_001", "TurnOnRequest")

# Turn off device
client.control_device("light_001", "TurnOffRequest")
```

---

### 3. control_air_conditioner

**Description:** Control air conditioner temperature and mode.

**Parameters:**
- `device_id` (string, required): Air conditioner device ID (AIR_CONDITION category)
- `action` (string, required): Control action type
  - `"IncrementTemperatureRequest"`: Increase temperature
  - `"DecrementTemperatureRequest"`: Decrease temperature
  - `"SetTemperatureRequest"`: Set target temperature
  - `"SetModeRequest"`: Set working mode
- `temperature` (int, optional): Target temperature 16-32°C (for SetTemperatureRequest)
- `delta` (string, optional): Temperature change amount, default "1" (for Increment/Decrement)
- `mode` (string, optional): Working mode (for SetModeRequest)
  - `"COOL"`: Cooling mode
  - `"HEAT"`: Heating mode
  - `"AUTO"`: Auto mode
  - `"FAN"`: Fan only
  - `"DEHUMIDIFICATION"`: Dehumidify
  - `"SLEEP"`: Sleep mode

**Examples:**
```python
# Set temperature to 26°C
client.control_air_conditioner("ac_001", "SetTemperatureRequest", temperature=26)

# Increase temperature by 2°C
client.control_air_conditioner("ac_001", "IncrementTemperatureRequest", delta="2")

# Set cooling mode
client.control_air_conditioner("ac_001", "SetModeRequest", mode="COOL")

# Set heating mode
client.control_air_conditioner("ac_001", "SetModeRequest", mode="HEAT")
```

---

### 4. trigger_scene

**Description:** Trigger a smart home scene to control multiple devices at once.

**Parameters:**
- `scene_id` (string, required): Scene identifier (format: sceneid_xxx)

**Common Scenes:**
- Coming Home Mode (回家模式)
- Leaving Home Mode (离家模式)
- Sleep Mode (睡眠模式)
- Movie Mode (观影模式)

**Example:**
```python
client.trigger_scene("sceneid_coming_home")
```

---

## MCP Prompts Reference

The MCP service provides three specialized prompts:

### 1. device_control
**Purpose:** Device control assistant focused on controlling lights, switches, curtains, etc.

**When to use:** When user wants to control specific device types (turn on/off lights, switches)

### 2. scene_trigger
**Purpose:** Scene control assistant for managing preset automation scenes

**When to use:** When user wants to execute scenes like "Coming Home", "Sleep Mode"

### 3. smart_home_assistant
**Purpose:** Full-featured smart home assistant

**When to use:** When user needs comprehensive home automation (query + control + scenes)

## Common Use Cases

### Example 1: Morning Routine
```python
client = MxchipMCPClient()

# Turn on bedroom light
client.control_device("bedroom_light", "TurnOnRequest")

# Set AC to comfortable temperature
client.control_air_conditioner("bedroom_ac", "SetTemperatureRequest", temperature=24)

# Open curtains (if supported)
client.control_device("curtain_001", "TurnOnRequest")
```

### Example 2: Leaving Home
```python
# Trigger "Leaving Home" scene
client.trigger_scene("sceneid_leaving_home")

# Or manually turn off devices
client.control_device("living_room_light", "TurnOffRequest")
client.control_device("bedroom_ac", "TurnOffRequest")
```

### Example 3: Check All Devices
```python
result = client.list_home_devices_and_scenes()

for device in result.get('devices', []):
    status = device.get('status', 'Unknown')
    print(f"{device['name']}: {status}")
```

## Device Categories

| Category | Description | Control Methods |
|----------|-------------|-----------------|
| LIGHT | Smart lights | control_device (on/off) |
| AIR_CONDITION | Air conditioners | control_air_conditioner |
| SWITCH | Smart switches | control_device (on/off) |
| CURTAIN | Smart curtains | control_device (on/off) |
| SOCKET | Smart sockets | control_device (on/off) |

## Error Handling

```python
from mxchip_mcp_client import (
    MxchipMCPClient,
    AuthenticationError,
    InvalidParameterError,
    MxchipMCPError
)

try:
    client = MxchipMCPClient()
    client.control_device("device_001", "TurnOnRequest")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
    # Regenerate token
except InvalidParameterError as e:
    print(f"Invalid parameter: {e}")
    # Check parameters
except MxchipMCPError as e:
    print(f"MCP error: {e}")
    # Handle other errors
```

## Troubleshooting

**Authentication Errors:**
- Verify `MXCHIP_OAUTH_TOKEN` is set correctly
- Token should start with `oauth2_`
- Regenerate token at OAuth page if expired

**Device Not Found:**
- Always call `list_home_devices_and_scenes()` first
- Use exact `device_id` from the response
- For AC control, ensure device category is `AIR_CONDITION`

**Invalid Parameters:**
- Temperature range: 16-32°C
- Valid modes: COOL, HEAT, AUTO, FAN, DEHUMIDIFICATION, SLEEP
- Scene ID format: `sceneid_xxx`

## Security Notes

- OAuth token provides access to your smart home devices
- Keep token secure and never commit to version control
- Token has expiration time - regenerate when needed
- Use environment variables for token storage

## Resources

### scripts/
- **mxchip_mcp_client.py** - Official MCP client SDK
  - Implements JSON-RPC 2.0 protocol
  - All 4 MCP tools wrapped as Python methods
  - Complete error handling
  - Type hints and documentation

### references/
- **api_reference.md** - Detailed API documentation
  - JSON-RPC 2.0 protocol details
  - Complete parameter specifications
  - Error codes and handling
  - Advanced usage examples

---

## README

### Project Information

**Skill Name:** Mxchip Smart Control  
**Developer:** Shanghai MXCHIP Information Technology Co., Ltd. (上海庆科信息有限公司)  
**Version:** 1.0.2  
**License:** MIT-0 (Free to use, modify, and redistribute)  
**Protocol:** MCP (Model Context Protocol) + JSON-RPC 2.0  

### About MXCHIP

Shanghai MXCHIP Information Technology Co., Ltd. (上海庆科信息有限公司) is a leading Chinese IoT solution provider founded in 2005. The company specializes in:

- **IoT Hardware**: Wi-Fi modules, Bluetooth modules, IoT development boards
- **Cloud Services**: MXCHIP Cloud platform for device management
- **Smart Home**: Smart Plus APP for home automation
- **AI Integration**: MCP protocol support for AI assistants

### Smart Plus APP

**Smart Plus** (智家精灵) is MXCHIP's official smart home application that provides:

- Device Management: Add and configure smart devices
- Scene Automation: Create custom automation rules
- Remote Control: Control devices from anywhere
- Voice Control: Integration with AI assistants via MCP

**Download:**
- iOS: App Store search "Smart Plus" or "智家精灵"
- Android: Major app stores search "Smart Plus" or "智家精灵"

### Supported Devices

This skill supports all devices configured in Smart Plus APP, including:

- **Switches**: Smart plugs, power strips
- **Lights**: Smart bulbs, LED strips, ceiling lights
- **Air Conditioners**: Split ACs, central ACs
- **Sensors**: Temperature, humidity, motion (via scenes)
- **Curtains**: Smart curtain controllers
- **Other**: Any device added to Smart Plus APP

### API Access

**MCP Endpoint:** https://app.api.cloud.mxchip.com:2443/mcp  
**OAuth Token:** https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth

**Authentication:** OAuth2 Bearer Token  
**Format:** `oauth2_<your_token>`  
**Validity:** Token expires after certain period (regenerate as needed)

### Use Cases

#### For Home Users
- Control devices with natural language
- Trigger scenes with voice commands
- Monitor device status
- Automate daily routines

#### For Developers
- Build AI-powered smart home applications
- Integrate with OpenClaw ecosystem
- Create custom automation workflows
- Develop voice-controlled interfaces

### Technical Stack

**Client SDK:** Python 3.7+  
**Dependencies:** requests>=2.28.0  
**Protocol:** MCP with JSON-RPC 2.0 over HTTP  
**Authentication:** OAuth2 Bearer Token  

### Support & Resources

**Official Website:** https://www.mxchip.com/  
**Documentation:** See `references/api_reference.md` in this skill  
**OAuth Token:** https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth  
**GitHub:** https://github.com/mxchip  

### Contributing

This skill is developed and maintained by Shanghai MXCHIP Information Technology Co., Ltd. For issues, feature requests, or contributions:

1. **Issues:** Contact MXCHIP support team
2. **Feature Requests:** Submit via Smart Plus APP feedback
3. **Documentation:** See skill documentation in `scripts/` and `references/` directories

### Disclaimer

This skill is provided as-is for controlling devices configured in Smart Plus APP. Users must:
- Have a valid Smart Plus APP account
- Configure devices in the app before using this skill
- Configure devices in the app before using this skill
- Keep OAuth token secure and confidential
- Comply with MXCHIP's terms of service

### Changelog

**v1.0.2 (2026-03-23)**
- Fixed JSON parsing for MCP response structure
- Updated environment variable from ZHIJIA to MXCHIP
- Added comprehensive documentation
- Added Shanghai MXCHIP company information

**v1.0.1 (2026-03-23)**
- Initial release
- Support for 4 MCP tools
- Support for 3 MCP prompts

---

**© 2026 Shanghai MXCHIP Information Technology Co., Ltd. All rights reserved.**
