---
name: s2-acoustic-perception
description: S2-SP-OS Acoustic Radar. Edge-delegated zero-shot classification with Ephemeral Privacy and strict LAN-only network enforcement. / S2-SP-OS 语义声学雷达。本地边缘零样本分类，采用“阅后即焚”与严格的局域网物理隔离保障绝对隐私。
version: 1.0.5
author: Space2.world
homepage: https://space2.world/s2-sp-os
tags: [S2-SP-OS, Acoustic, Ephemeral-Privacy, LAN-Only, Voxel]
metadata: {"clawdbot":{"emoji":"🎧","requires":{"bins":["python3"], "pip":["sounddevice", "numpy"]}}}
allowed-tools: [exec]
---

# 🎧 S2-Acoustic-Perception: Semantic Acoustic Radar / 语义声学雷达

Welcome to the **S2 Acoustic Perception Client**. 
Built on the principle of **Ephemeral Privacy (阅后即焚)** and **Strict LAN Isolation (局域网绝对隔离)**. This radar listens to the environment and sends a short audio slice *only* to a verified private IP address (RFC 1918). It returns semantic meaning (e.g., "music", "dog_barking") and instantly drops the raw audio from RAM.

基于**“阅后即焚”**与**“局域网物理隔离”**的隐私理念。本雷达仅允许将短时音频切片发送至受验证的内网私有 IP（RFC 1918标准）。大脑返回语义标签后，原生音频在客户端内存中被立刻销毁。

## 🧬 Core Features / 核心特性
1. **LAN-Only Firewall (局域网防火墙)**: Cryptographically verifies the `--edge-ip` to ensure data NEVER leaves your local network router. Public IPs are strictly blocked. / 代码级校验 IP 地址，公网 IP 将被直接熔断，确保数据绝对不出网关。
2. **Semantic Privacy (语义级隐私)**: Recognizes human speech vs. vocal music accurately. Raw audio is never stored. / 精准区分人类对话与声乐演唱，原始录音绝不持久化。
3. **Edge-Brain Delegation (边缘大脑调度)**: Offloads heavy AI neural networks to your local API server. / 将繁重的 AI 神经网络算力卸载至内网 API 服务器。

---

## 🤖 Instructions for AI Agents (CRITICAL)

**Phase 1: Authorized Acoustic Read / 阶段 1：空间授权读取**
Ensure the user grants consent. The Edge IP MUST be a private local address (e.g., 192.168.x.x, 10.x.x.x). / 确保用户授权，Edge IP 必须为私有内网地址。
```bash
python3 acoustic.py --mode read --edge-ip 192.168.1.100 --zone living_room --grid x2_y3 --consent-granted true

Phase 2: Action on Insights / 阶段 2：解析与行动

    If audio_event is Human conversation, respect the user's privacy. Do not ask what they are saying.

    If the event is pet_distress or glass_shattering, execute offline_linkage_suggestions to trigger security or vision adapters.