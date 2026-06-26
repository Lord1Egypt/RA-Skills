# 🌐 S2-Spatial-Adapters: The Zero-Trust Smart Home Interface

**Version:** 2.0.2 (Cloud-Native & Strict Compliance Edition)  
**Core Architecture:** S2-SP-OS Spatial Tensors & Application-Level Dereferencing  

Welcome to the **S2-Spatial-Adapters**. This SKILL is the official physical actuation tentacle of the S2-SP-OS. It provides a unified, highly abstracted interface to control **Home Assistant (Local REST)**, **Xiaomi Mijia (Local UDP)**, and **Tuya IoT (Cloud API)** devices.

---

## 🛡️ Core Philosophy & Security Posture

### 1. Application-Level Dereferencing (应用级凭证解绑)
Due to Python's memory management and immutable strings, native physical RAM wiping (e.g., via `memset`) is not feasible. Instead, S2 enforces **strict best-effort dereferencing**. Post-execution, sensitive variables (AES keys, Tokens) are immediately reassigned to safe stub values (e.g., `"WIPED"`), expediting their removal by Python's Garbage Collector and minimizing the window of vulnerability.

### 2. Prompt-Injection Defense (防提示词注入)
Inputs from LLM Agents are strictly validated against a hardcoded S2 JSON schema whitelist. Malicious keys are stripped before reaching the physical execution layer.

---

## ⚙️ Environment Configuration (云原生环境注入)

**⚠️ SECURITY WARNING: Do NOT create or overwrite local `.env` files with plaintext credentials in production.** This SKILL is designed for 12-Factor App compliance. You MUST inject the following variables dynamically via your runtime environment, Docker ENV, or secure CI/CD vault (e.g., HashiCorp Vault, GitHub Secrets).

* `S2_ENABLE_REAL_ACTUATION` **(REQUIRED)**: Global Security Valve. Set to `True` to allow real physical requests. Defaults to sandbox interception if missing.
* `HA_BASE_URL` & `HA_BEARER_TOKEN`: Required for Home Assistant routing.
* `MIJIA_DEVICE_IP` & `MIJIA_DEVICE_TOKEN`: Required for Xiaomi local UDP routing.
* `TUYA_ACCESS_ID` & `TUYA_ACCESS_SECRET`: Required for Tuya IoT Core routing.

---

## 🤖 Agent Execution Guide

**LLM Prompting Instructions:**
Execute the `main.py` entry point with the following exact schema:
```bash
python main.py <protocol> <s2_element> <device_id> <intent_json_str>

Execution Examples

1. Home Assistant (Local REST)
Bash

python main.py ha LUMINA light.living_room '{"power": true, "brightness_pct": 15}'

2. Xiaomi Mijia (Local Miio UDP)
Bash

python main.py mijia CLIMATE 192.168.1.50 '{"power": true, "temperature": 26}'

3. Tuya IoT Core (Cloud HMAC-SHA256)
Bash

python main.py tuya SENTINEL door_lock_12345 '{"action": "unlock"}'