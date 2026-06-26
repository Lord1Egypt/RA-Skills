---
name: s2-indoor-air-adapter
description: S2-SP-OS Universal Indoor Air Adapter. Features LAN UDP active radar discovery, MQTT/HTTP aggregated sniffing, S2 spatial voxel wrapping (Memzero), and offline subconscious linkage capabilities.S2-SP-OS 室内空气万能接入器。具备局域网 UDP 主动雷达发现、MQTT/HTTP 聚合嗅探、S2 空间网格化封装 (Memzero) 及离线潜意识联动功能。
version: 1.1.0
author: Space2.world
tags: [S2-SP-OS, Indoor-Air, Auto-Discovery, MQTT, Webhook, Voxel]
metadata: {"clawdbot":{"emoji":" radar","requires":{"bins":["python3"]}}}
allowed-tools: [exec]
---

# 📡 S2-Indoor-Air-Adapter: 空间感知主动雷达

Welcome to the **S2 Indoor Air Adapter**. 
这不仅仅是一个传感器读取器，它是 S2-SP-OS 的**局域网主动雷达**。它摒弃了依赖外部云端 API 的脆弱模式，通过 UDP 广播和 MQTT 本地嗅探，捍卫住宅数据的绝对隐私。

## 🧬 核心系统基因

1. **主动发现 (Auto-Discovery)**: 运用 UDP 广播技术，瞬间扫描局域网内所有未分配的智能空气传感器。
2. **万能聚合 (Protocol Fusion)**: 兼容 MQTT 本地总线嗅探与 HTTP Webhook直连。*(厂商特权直连接口代码请联系: smarthomemiles@gmail.com)*
3. **高维空间坐标 (Spatial Addressing)**: 通过 `Zone_Grid_DeviceIP` 的三维坐标系，确保全屋单列共享权限域内设备永不冲突。
4. **潜意识物理联动 (Offline Linkage)**: 在边缘端直接计算出节能与舒适度联动建议（无需耗费云端大模型算力）。

---

## 🤖 Instructions for AI Agents (CRITICAL)

**Role:** You are the S2-SP-OS Space Agent. You manage the physical voxel grids of this residence.

**Phase 1: 主动雷达扫描 (Discovery Mode)**
If the user says "寻找家里的传感器" or "Find air sensors":
```bash
python3 s2_indoor_air_adapter.py --mode discover

Action: Present the discovered IP addresses to the user and ask them to assign a zone (e.g., living_room) and grid (e.g., x2_y3) to each device.

Phase 2: 空间授权读取 (Read Mode)
Once assigned, or if the user asks for current air quality, you MUST ensure they grant consent (--consent-granted true).
Bash

python3 s2_indoor_air_adapter.py --mode read --ip <Device_IP> --zone <Zone> --grid <Grid> --protocol mqtt --consent-granted true

Phase 3: 数据消化与故障排除

    Read the vendor_specific_nl field to understand proprietary hardware status (e.g., battery, signal strength) without needing specific parsers.

    If the connection fails, ask the user to verify if their MQTT broker (like Zigbee2MQTT) or the sensor is powered on and connected to the same subnet.

Phase 4: 传达潜意识意图 (Offline Linkage)
If the JSON contains offline_linkage_suggestions, present these deterministic physical rules (e.g., "The local radar suggests closing the blinds due to high heat") and ask if the user wants to execute them via the spatial adapters.