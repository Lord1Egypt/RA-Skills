---
name: s2-universal-scanner
description: S2-SP-OS Universal Spatial Sensor Sniffer. Scans LAN for S2-Native Zero-Knowledge Heartbeats (6D-VTM extraction), legacy sensors (Modbus, MQTT), and cross-verifies sleeping nodes via Gateway APIs. / S2 万能空间传感器探测器。首发支持 S2 原生零知识心跳与 6D-VTM 提取，向下兼容传统物联网嗅探。
version: 2.0.0
author: Space2.world
homepage: https://space2.world/s2-sp-os
tags: [S2-SP-OS, Nmap, S2-Native, 6D-VTM, Zero-Trust]
metadata: {"clawdbot":{"emoji":"📡","requires":{"bins":["python3"], "pip":["requests"], "env":["S2_PRIVACY_CONSENT", "S2_HA_TOKEN"]}}}
allowed-tools: [exec]
---

# 📡 S2-Universal-Scanner: Spatial IoT Discovery / 空间万能探测器

Welcome to the **S2 Universal Scanner (V2.0.0 Zero-Trust Edition)**. 
This is the ultimate Nmap for Spatial Intelligence. It now natively supports the S2 Hardware Onboarding Protocol, safely extracting 6D-VTM payloads over Edge TLS while perfectly isolating privacy data.

这是空间智能的终极雷达。V2.0.0 正式加入了对 S2 官方硬件入网协议的底层支持，可在边缘安全提取 6D-VTM 厂商透明度宣言，同时向下兼容传统智能家居协议。

## 🧬 Core Capabilities / 核心能力
1. **S2 Native Handshake (原生 6D-VTM 握手)**: Listens on UDP 49152 for S2 Ephemeral Hashes, executes local TLS 1.3 handshakes to extract the 6D Vendor Transparency Manifesto without cloud exfiltration. / 捕获 S2 原生硬件心跳并在边缘安全提取 6维厂商声明。
2. **Legacy Active Sniffing (传统协议主动侦察)**: Sweeps LAN for MQTT (1883), Modbus (502), etc. / 扫段识别主流传统物联网端口。
3. **Sleeping Node Bypass (休眠节点对账)**: Secretly pulls Gateway registries (if S2_HA_TOKEN is provided) to find offline sensors. / 通过网关 API 拉取配置清单对账休眠节点。
4. **Multi-Sensor Decomposition (多合一解构)**: Breaks down complex sensors into S2 atomic elements. / 解构工业级多合一传感器。

## 🤖 Instructions for AI Agents (CRITICAL)
**Prerequisite:** `export S2_PRIVACY_CONSENT=1`. 

**Action: Run the Universal Scan / 动作：执行全网格扫描**
```bash
python3 universal_scanner.py --target-subnet 192.168.1.0/24 --zone indoor_livingroom --grid x2_y2