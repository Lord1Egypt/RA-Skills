# HomeKit Control Guide (homebridge-mcp-server)

## Overview

[homebridge-mcp-server](https://github.com/mp-consulting/homebridge-mcp-server) is an MCP server for [Homebridge](https://homebridge.io) that allows AI agents to control HomeKit accessories, manage plugins, edit configuration, and monitor the Homebridge server.

**Repository:** https://github.com/mp-consulting/homebridge-mcp-server
**Language:** TypeScript (Node.js)
**License:** MIT
**Install:** `npm install -g @mp-consulting/homebridge-mcp-server`

## Architecture

```
AI Agent → MCP (stdio) → homebridge-mcp-server → Homebridge REST API → HomeKit accessories
```

- **Cross-platform** — runs on macOS, Linux, Windows (anywhere Node.js runs)
- **No re-pairing** — controls devices already paired to Homebridge
- **MCP standard** — works with Claude Desktop, Claude Code, and any MCP-compatible agent

## Prerequisites

1. **Homebridge** installed and running
2. **homebridge-config-ui-x** plugin installed (provides the REST API)
3. **Node.js 18+**

## Installation

### Step 1: Install Homebridge

```bash
# Option A: Official Homebridge Raspberry Pi Image (recommended for dedicated device)
# Download from https://homebridge.io/download

# Option B: Docker
docker run -d --name homebridge --restart=unless-stopped \
  --net=host \
  -e HOMEBRIDGE_CONFIG_UI=1 \
  -e HOMEBRIDGE_CONFIG_UI_PORT=8581 \
  -v ~/homebridge:/homebridge \
  homebridge/homebridge:latest

# Option C: npm global install
npm install -g homebridge homebridge-config-ui-x
```

### Step 2: Install MCP Server

```bash
npm install -g @mp-consulting/homebridge-mcp-server
```

### Step 3: Configure MCP

Set environment variables:

```bash
export HOMEBRIDGE_URL="http://192.168.1.100:8581"
export HOMEBRIDGE_USERNAME="admin"
export HOMEBRIDGE_PASSWORD="your-password"
```

Or create `.env` file:
```
HOMEBRIDGE_URL=http://192.168.1.100:8581
HOMEBRIDGE_USERNAME=admin
HOMEBRIDGE_PASSWORD=your-password
```

## MCP Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "homebridge": {
      "command": "homebridge-mcp-server",
      "env": {
        "HOMEBRIDGE_URL": "http://192.168.1.100:8581",
        "HOMEBRIDGE_USERNAME": "admin",
        "HOMEBRIDGE_PASSWORD": "your-password"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add homebridge -- homebridge-mcp-server
```

Then set environment variables in shell or `.env` file.

### OpenCode

Add to `opencode.json`:

```json
{
  "mcp": {
    "homebridge": {
      "command": ["homebridge-mcp-server"],
      "env": {
        "HOMEBRIDGE_URL": "http://192.168.1.100:8581",
        "HOMEBRIDGE_USERNAME": "admin",
        "HOMEBRIDGE_PASSWORD": "your-password"
      }
    }
  }
}
```

## Available MCP Tools

### Accessories

| Tool | Description |
|------|-------------|
| `list_accessories` | List all accessories with current state. Filter by `room`, `type`, `name`, `manufacturer`, `excludeManufacturer` |
| `get_accessory` | Get detailed info for a specific accessory |
| `set_accessory` | Control an accessory (on/off, brightness, temperature, etc.) |
| `get_accessory_layout` | Get room layout from Homebridge UI |

### Server

| Tool | Description |
|------|-------------|
| `get_homebridge_status` | Check if Homebridge is running |
| `get_server_status` | Server version, uptime, Node.js version, OS details |
| `restart_homebridge` | Restart the Homebridge service |
| `get_pairing_info` | Get HomeKit pairing code / QR info |
| `get_cached_accessories` | List cached accessories |
| `remove_cached_accessory` | Remove a specific cached accessory |
| `reset_cached_accessories` | Reset all cached accessories |

### Configuration

| Tool | Description |
|------|-------------|
| `get_config` | Read the current config.json |
| `update_config` | Update config.json (full replacement) |

### Plugins

| Tool | Description |
|------|-------------|
| `list_plugins` | List installed plugins |
| `search_plugins` | Search npm for Homebridge plugins |
| `lookup_plugin` | Get details about a specific plugin |
| `get_plugin_versions` | Get available versions for a plugin |
| `get_plugin_config_schema` | Get the configuration schema for a plugin |
| `get_plugin_changelog` | Get the changelog for a plugin |

### System

| Tool | Description |
|------|-------------|
| `get_system_info` | Host system info (CPU, memory, OS) |

## Example Agent Interactions

```
User: "Turn off the living room lights"
Agent: [calls set_accessory with living room lights, on=false]

User: "What's the temperature in the bedroom?"
Agent: [calls list_accessories, filters by room=bedroom, type=temperature_sensor]

User: "Set thermostat to 21 degrees"
Agent: [calls set_accessory with thermostat, target_temperature=21]

User: "Is Homebridge running?"
Agent: [calls get_homebridge_status]

User: "Search for a plugin for Philips Hue"
Agent: [calls search_plugins with query="philips hue"]
```

## Supported Accessory Types

Lights, switches, thermostats, locks, doors, garage doors, fans, window coverings, outlets, sensors (motion, contact, temperature, humidity, light level, battery), cameras, doorbells.

## Adding Devices to Homebridge

Homebridge uses **plugins** to bridge non-HomeKit devices into HomeKit:

1. Open Homebridge UI (`http://<host>:8581`)
2. Go to Plugins → Search
3. Install the plugin for your device brand (e.g., "homebridge-mi-smart-home" for Xiaomi)
4. Configure the plugin with your device credentials
5. Devices appear as HomeKit accessories

Common plugins:
| Plugin | Devices |
|--------|---------|
| `homebridge-mi-smart-home` | Xiaomi/Mijia devices |
| `homebridge-hue` | Philips Hue |
| `homebridge-tuya` | Tuya/Smart Life devices |
| `homebridge-ring` | Ring cameras/doorbells |
| `homebridge-nest` | Nest thermostats |
| `homebridge-ewelink` | Sonoff/eWeLink devices |
| `homebridge-govee` | Govee lights |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Connection refused` | Homebridge not running | Start Homebridge, check port |
| `Unauthorized` | Wrong credentials | Check username/password in env vars |
| `No accessories found` | No plugins configured | Install device plugins in Homebridge UI |
| `Timeout` | Network issue | Check HOMEBRIDGE_URL is reachable |
