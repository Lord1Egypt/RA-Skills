# 🧓 S2-Eldercare-mmWave-Monitor: DSP & Secure Actuation Engine
# S2 老年健康监测插件 (微多普勒 DSP 与安全物理致动版)
*v1.1.0 | SecOps & Hardware Integration Edition (English / 中文)*

Welcome to the **Sensory Tentacle Series** of the S2-SP-OS. This SKILL bridges high-resolution mmWave DSP with physical smart home actuation, heavily focused on user safety and zero-trust execution.

🛡️ 1. Security & Safety First (安全与执行声明)
**WARNING: Automatic actuation of physical environments (e.g., unlocking doors, overriding HVAC) carries inherent real-world risks.**
**警告：自动触发物理环境动作（如解锁大门、强启空调）具有固有的现实世界风险。**

To comply with strict SecOps and safety standards, this SKILL operates in **Dry-Run (Safe Mode) by default**. 
为了符合严苛的安全操作规范，本插件**默认运行在安全沙盒模式（Dry-Run）下**：
* When `S2_ENABLE_REAL_ACTUATION=False` (Default), the system runs the entire DSP algorithm (STFT, Fall Detection) but intercepts all outbound HTTP REST requests to the Home Assistant API. It only prints the routing intents to the console.
* 当环境变量为 False 时，系统将拦截所有发往物理网关的 HTTP 真实请求，仅在控制台打印模拟意图。

**To enable REAL physical actuation (开启真实物理控制):**
You must explicitly export the following environment variables. Do this *only* in a trusted local environment with user consent.
您必须显式声明以下环境变量（请仅在受信任的且获得用户授权的本地局域网环境中开启）：
bash
export S2_ENABLE_REAL_ACTUATION="True"
export HA_BASE_URL="http://your-ha-ip:8123/api"
export HA_BEARER_TOKEN="your_ha_access_token"

🧮 2. The Micro-Doppler DSP Architecture (微多普勒 DSP 架构)

This module simulates and processes Frequency Modulated Continuous Wave (FMCW) data to detect falls. We use scipy.signal.stft to convert the 1D echo into a 2D Time-Frequency Spectrogram, searching for rapid negative Doppler shifts indicative of a fall.

🔌 3. The Physical Actuator (物理执行层)

When a fall is verified by the DSP engine, the system dispatches HTTP POST payloads to the S2 Message Bus (via Home Assistant):

    POST /api/services/lock/unlock -> Unlocks the front door for emergency responders.

    POST /api/services/light/turn_on -> Overrides sleep lighting to 100% Daylight.

⚙️ 4. Installation (依赖安装)

Ensure all dependencies (numpy, scipy, matplotlib, requests) are installed:
Bash
pip install -r requirements.txt
python skill.py