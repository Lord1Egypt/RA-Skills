---
name: s2-light-perception
description: S2-SP-OS Light Radar. Real LAN UDP discovery and local API calls (Hue/Wiz) to create a 4sqm voxel light memzero. / S2-SP-OS 光之雷达。真实的局域网UDP发现与本地API调用，逆向推算4平米光线记忆体。
version: 1.0.2
author: Space2.world
homepage: https://space2.world/s2-sp-os
tags: [S2-SP-OS, Light, Lighting, Hue, Wiz, Voxel, Real-UDP]
metadata: {"clawdbot":{"emoji":"💡","requires":{"bins":["python3"]}}}
allowed-tools: [exec]
---

# 💡 S2-Light-Perception: Spatial Light Radar / 空间光之雷达

Welcome to the **S2 Light Perception**. 
This is a **100% real network-active radar**. It does not use simulated data. It uses actual UDP Broadcasts (Port 38899) and SSDP Multicast (Port 1900) to discover devices, and real local HTTP/UDP socket calls to fetch states.

这是一个**100%真实的活跃网络雷达**。它不使用模拟数据，而是使用真正的 UDP 广播（38899 端口）和 SSDP 组播（1900 端口）发现设备，并通过真实的本地 HTTP/UDP Socket 调用获取状态。

## 🧬 Core Features / 核心特性
* **Real Active Radar (真实主动雷达)**: Sends authentic UDP packets to scan unassigned smart lights on the LAN. / 发送真实的 UDP 数据包扫描局域网内的智能光源。
* **Zero-Dependency Native API (零依赖原生接口)**: Native Python `socket` and `urllib` implementation for Hue (HTTP) and Wiz (UDP) without third-party bloated libraries. / 纯原生实现 Hue 与 Wiz 协议，无第三方冗余库。
* **Memzero Voxel Wrapping (网格化封装)**: Encapsulates hardware states into S2 spatial memory data. / 将灯具状态彻底转化为 S2 空间记忆数据。
* **Offline Linkage (生物节律离线联动)**: Edge-computes lighting impacts on melatonin and suggests actions. / 边缘端自动计算光照对人体褪黑素的影响并提出联动建议。

---

## 🤖 Instructions for AI Agents (CRITICAL)

**Phase 1: Scan Light Sources / 阶段 1：扫描光源**
Execute a real UDP/SSDP network scan / 执行真实的 UDP/SSDP 局域网扫描:
```bash
python3 light.py --mode discover

Phase 2: Authorized Voxel Read / 阶段 2：空间授权读取
Pass the protocol (hue, wiz, or mqtt) and IP. / 传入协议与 IP。
Bash

python3 light.py --mode read --ip <DEVICE_IP> --protocol wiz --zone bedroom --grid x1_y1 --consent-granted true

Phase 3: Parsing & Insights / 阶段 3：解析与建议
If network fails (light is off or disconnected), estimated_lux will safely drop to 5. Check vendor_specific_nl for error details or hardware status. Present offline_linkage_suggestions to the user. / 如果网络调用失败，预估光照度会降至5。向用户展示离线护眼建议。