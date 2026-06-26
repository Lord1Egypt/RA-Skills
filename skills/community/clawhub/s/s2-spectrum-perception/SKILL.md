---
name: s2-spectrum-perception
description: S2-SP-OS Spectrum Radar. Pure, passive spatial perception using GPIO/UART with explicit OS environment consent (S2_PRIVACY_CONSENT) and quantized biometrics. / S2 波段雷达。纯粹的被动空间感知探针，显式声明环境变量授权。
version: 2.0.3
author: Space2.world
homepage: https://space2.world/s2-sp-os
tags: [S2-SP-OS, Spectrum, mmWave, UART, Passive-Sensor]
# [CRITICAL FIX]: 显式向沙盒声明所需的系统环境变量，消除隐式依赖
metadata: {"clawdbot":{"emoji":"🌊","requires":{"bins":["python3"], "pip":["pyserial"], "env":["S2_PRIVACY_CONSENT"]}}}
allowed-tools: [exec]
---

# 🌊 S2-Spectrum-Perception: Spatial mmWave Radar / 空间毫米波雷达

Welcome to the **S2 Spectrum Perception**. 
This is a **strictly passive** spatial sensing tool. It reads commercial mmWave modules (via GPIO or UART) to extract occupancy and quantized health data. It makes ZERO assumptions about actuation and executes NO cross-device triggers.

这是一个**绝对被动**的空间感知工具。它仅读取毫米波模块获取占位与量化体征数据，绝不越权进行任何跨设备触发或执行决策。

## 🧬 Core Features / 核心特性
1. **Declared OS-Level Consent (显式系统级授权)**: Explicitly requires the `S2_PRIVACY_CONSENT=1` environment variable. 
2. **Pure Perception (纯粹感知)**: Acts solely as a sensory organ. Outputs cleanly formatted `s2_chronos_memzero` data for the Agent to interpret. / 仅作为感知器官，输出纯净的网格记忆体数据供 Agent 解析。
3. **Biometric Quantization (生物隐私量化)**: Exact BPMs are safely destroyed at the hardware edge. / 精确生物数据在硬件边缘即刻销毁。

---

## 🤖 Instructions for AI Agents (CRITICAL)

**Prerequisite:** The environment MUST have `S2_PRIVACY_CONSENT=1` set.

**Phase 1: Read Hardware State / 阶段 1：直读硬件状态**
```bash
python3 spectrum.py --mode gpio --zone bedroom --grid x1_y1

Phase 2: Advanced UART Vital Scan / 阶段 2：高级串口体征扫描
Bash

python3 spectrum.py --mode uart --port /dev/ttyUSB0 --zone bedroom --grid x1_y1

Phase 3: Cognitive Decision (大脑决策)
Read the s2_chronos_memzero. As the Agent, YOU must decide what to do next based on your system prompts and examples. The radar will not suggest actions for you. / 读取数据后，作为大脑的你必须自行决定下一步行动，雷达探针不再提供行动建议。


---