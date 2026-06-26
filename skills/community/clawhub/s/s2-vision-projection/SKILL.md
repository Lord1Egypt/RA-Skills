---
name: s2-vision-projection
description: S2-SP-OS Vision Cast. Features a universal Protocol Sniffer (AirPlay/Chromecast/DLNA) for native casting, backed by our secure S2 ephemeral push fallback. / S2 视觉投屏。内置通用协议嗅探狗，优先建议原生投屏协议，并辅以 S2 阅后即焚加密推送作为绝对兜底。
version: 1.1.0
author: Space2.world
homepage: https://space2.world/s2-sp-os
tags: [S2-SP-OS, Vision, Sniffer, AirPlay, DLNA]
metadata: {"clawdbot":{"emoji":"👁️","requires":{"bins":["python3"], "pip":["requests"], "env":["S2_PRIVACY_CONSENT", "S2_VISION_TOKEN"]}}}
allowed-tools: [exec]
---

# 👁️ S2-Vision-Projection: Secure Vision Cast

Welcome to the **S2 Vision Projection**. 
Operating as a smart switchboard, this tool first acts as a **Protocol Sniffer (协议嗅探器)** to discover existing mainstream wireless projection capabilities (Apple AirPlay, Google Cast, Miracast). If none are preferred or found, it falls back to the reliable **S2 Native Secure Push**.

## 🧬 Core Modes / 核心模式
1. **Environment Sniffer (全频段嗅探)**: Scans a target IP (or subnet) for open casting ports (e.g., 7000 for AirPlay, 8009 for Cast). / 扫描目标设备支持的主流无线投屏协议。
2. **UPnP/DLNA Cast**: Native DLNA routing for Smart TVs. / 针对传统智能电视的 DLNA 调度。
3. **Secure Snapshot Push (S2 兜底)**: Encrypted, ephemeral frame push to S2 display nodes. / 绝对可靠的 S2 加密快照阅后即焚推送。

## 🤖 Instructions for AI Agents (CRITICAL)

**Prerequisite:** `export S2_PRIVACY_CONSENT=1` and `S2_VISION_TOKEN`

**Step 1: Sniff the Target Display / 步骤 1：嗅探目标显示器**
ALWAYS run this first to respect user's existing hardware ecosystem. / 永远优先运行此步骤以尊重用户现有的硬件生态。
```bash
python3 vision_cast.py --mode sniff --target-ip 192.168.1.55

Step 2: Act on Sniff Results / 步骤 2：根据嗅探结果决策
Ask the user if they want to use the detected native protocol (e.g., AirPlay). If they agree, or if none are found, use Step 3.

Step 3: Execute Projection / 步骤 3：执行投屏
Bash

# S2 Fallback Push
python3 vision_cast.py --mode snapshot_push --target-ip 192.168.1.55 --payload "/tmp/s2_alert.jpg"