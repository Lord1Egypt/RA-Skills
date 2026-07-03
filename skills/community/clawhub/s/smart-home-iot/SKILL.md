---
name: Smart Home IoT Control
slug: smart-home-iot
description: 一站式智能家居设备管理与自动化编排技能。支持Home Assistant、米家、涂鸦智能等主流平台，通过自然语言控制灯光、温控、安防、窗帘等设备，支持场景联动与定时任务。兼容MQTT/Zigbee/Matter协议，覆盖全球主流智能家居生态。
version: 1.0.0
author: ai-gaoqian
tags:
  - smart-home
  - iot
  - home-automation
  - mqtt
  - matter
metadata:
  openclaw:
    requires:
      - python>=3.10
      - homeassistant-api
---

# Smart Home IoT Control

Unified smart home device management and automation skill for OpenClaw. Control lights, thermostats, security systems, curtains, and appliances across multiple platforms using natural language.

## Supported Platforms

| Platform | Protocol | Region |
|----------|----------|--------|
| Home Assistant | REST/WebSocket | Global |
| Mi Home (米家) | MiIO | China/Asia |
| Tuya Smart | Tuya Cloud API | Global |
| SmartThings | Samsung API | Global |
| Apple HomeKit | HAP | Global |

## Core Capabilities

### Device Discovery & Status
- Auto-discover devices on local network
- Real-time status polling (online/offline, power, brightness, temperature)
- Device categorization by room and type
- Health monitoring and battery level alerts

### Natural Language Control
```
"Turn off all lights in the living room"
"Set bedroom temperature to 22°C"
"Lock all doors and arm the security system"
"Dim the dining room lights to 30%"
```

### Scene Automation
- Create custom scenes (e.g., "Movie Night": dim lights + close curtains + turn on TV)
- Time-based schedules (sunrise/sunset triggers)
- Conditional triggers (motion detected → turn on lights)
- Multi-condition AND/OR logic

### Energy Management
- Power consumption tracking per device
- Usage patterns analysis
- Energy-saving recommendations
- Solar/battery integration monitoring

## Protocols Support
- **MQTT 3.1.1/5.0**: Full pub/sub with TLS
- **Zigbee 3.0**: Via ZHA or zigbee2mqtt
- **Matter 1.2**: Thread/Wi-Fi commissioning
- **Z-Wave**: Via controller gateway
- **Bluetooth LE**: Sensor data collection

## Security
- Local-first architecture (no cloud dependency for core functions)
- End-to-end encryption for remote access
- OAuth 2.0 device authorization
- Role-based access control (admin/family/guest)

## Usage Examples

```yaml
# Discover all devices
action: discover
output: device_list.yaml

# Create a scene
scene: good_morning
triggers:
  - time: "07:00"
  - condition: weekday
actions:
  - device: bedroom_curtains
    command: open
    level: 100
  - device: kitchen_light
    command: on
    brightness: 80
  - device: coffee_maker
    command: on
```
