# 🌌 S2-Spatial-Adapters: The Zero-Trust Smart Home Interface

[![Version](https://img.shields.io/badge/version-2.0.5-blue.svg)](#)
[![Security](https://img.shields.io/badge/SecOps-Passed-success.svg)](#)
[![Compliance](https://img.shields.io/badge/CloudNative-Ready-green.svg)](#)
[![Agent](https://img.shields.io/badge/OpenClaw-Compatible-orange.svg)](#)

Welcome to the **S2 Spatial Adapters**. This is not your traditional smart home script. 
Built on the principles of the **S2-SP-OS (Spatial Operating System)**, this tool unifies **Home Assistant (REST)**, **Xiaomi Mijia (Local UDP)**, and **Tuya (Cloud OpenAPI)** under a single, highly abstracted, and cryptographically secure interface designed exclusively for Autonomous AI Agents.

---

## 🚀 The Paradigm Shift: S2 Spatial Tensors
Stop forcing your LLMs to memorize complex vendor-specific APIs (like Mijia `siid/piid` or Tuya `DP Codes`). The S2 architecture allows your AI Agent to operate in High-Dimensional Spatial Tensors. You speak intents; we handle the protocols.

* 💡 **`LUMINA` (Lighting)**: Controls power, brightness_pct, color_temp.
* ❄️ **`CLIMATE` (HVAC)**: Controls power, temperature, hvac_mode.
* 🛡️ **`SENTINEL` (Security)**: Controls door locks and alarms.
* 🐾 **`PET_CARE` (Welfare)**: Controls automated pet feeders.

---

## 🧠 Deploying the S2 Commander Agent (Out-of-the-Box)
Physical adapters are useless without a brain. We have included `s2_commander.json`, a plug-and-play Agent Template designed for **OpenClaw / AutoGen** frameworks.

### Quick Start for AI Agents:
1. **Import the Agent**: Load `s2_commander.json` into your framework. *(Note: The temperature is strictly locked at `0.1` to enforce deterministic JSON generation and completely eliminate hallucinated arguments).*
2. **Mount the Tool**: Ensure the `s2-spatial-adapters` directory is accessible to the Agent.
3. **Provide Context**: Tell the agent your device mapping (e.g., "Living room AC is Mijia IP 192.168.1.50"). Watch it autonomously map natural language to physical actuations.

---

## 🛡️ Enterprise SecOps & Compliance (V2.0.5)
We have completely overhauled the security architecture to protect your physical home from LLM hallucinations and network attacks. This package has passed rigorous Red Team auditing:

1. **Anti-Prompt-Injection**: Strict JSON schema whitelisting strips malicious commands hallucinated by AI Agents before they reach the physical layer.
2. **Application-Level Dereferencing**: Post-actuation, sensitive AES keys and Access Tokens are immediately un-bound and reassigned to safe stubs to expedite Python Garbage Collection.
3. **Data Leakage Prevention (DLP)**: All sensitive payloads and internal IP mappings are strictly redacted (`[REDACTED]`) in standard console outputs to protect your living habits from log aggregators.
4. **Hardcore SSRF & Endpoint Defense**: Deep DNS/IP resolution blocks UDP/HTTP DNS Rebinding attacks. Tuya endpoints are locked to a strict official whitelist.
5. **Cloud-Native Provisioning**: We strictly oppose storing plaintext credentials in local files. Zero file I/O. All secrets must be injected via secure OS-level runtime environments.

---

## 🛠️ Installation & Execution

### 1. Install Pinned Dependencies
```bash
pip install -r requirements.txt

2. Cloud-Native Environment Injection

⚠️ SECURITY WARNING: Do NOT create local .env files. You MUST inject the following variables dynamically via your runtime environment, Docker ENV, or secure CI/CD vault:

    S2_ENABLE_REAL_ACTUATION (REQUIRED): Global Security Valve. Must be True to allow real physical requests. Defaults to Dry-Run sandbox.

    HA_BASE_URL & HA_BEARER_TOKEN: Conditionally required for HA routing.

    MIJIA_DEVICE_IP & MIJIA_DEVICE_TOKEN: Conditionally required for Mijia UDP.

    TUYA_ACCESS_ID & TUYA_ACCESS_SECRET: Conditionally required for Tuya routing.

3. Agent Execution Syntax

The AI Agent (or human developer) executes the actuator via:
Bash

python main.py <protocol> <s2_element> <device_id> '<intent_json>'

Examples:
Bash

# S2 LUMINA -> Home Assistant
python main.py ha LUMINA light.living_room '{"power": true, "brightness_pct": 15}'

# S2 CLIMATE -> Xiaomi Mijia
python main.py mijia CLIMATE 192.168.1.50 '{"power": true, "temperature": 26}'

# S2 PET_CARE -> Tuya IoT
python main.py tuya PET_CARE feeder_789 '{"feed_portions": 2}'

⚖️ Liability Disclaimer

By injecting S2_ENABLE_REAL_ACTUATION=True into your environment, you explicitly authorize the Autonomous AI Agent to actuate your physical systems (HVAC, locks, etc.). Space2.world assumes zero liability for physical damage, injury, or security breaches resulting from autonomous AI behavior. Use in heavily monitored environments.