---
name: zke-trading
description: ZKE AI Master Trader (Official). Control spot and futures trading, manage assets, and access real-time market data on ZKE Exchange.
version: 1.0.13
emoji: 📈
homepage: https://support.zke.com/skills/
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - npm
      env:
        - ZKE_API_KEY
        - ZKE_SECRET_KEY
    primaryEnv: ZKE_API_KEY
---

# ZKE Exchange Trading Skill (Official)

**The Official OpenClaw (MCP) implementation for secure, conversational trading on ZKE Exchange.**

---

## 🔒 Security Architecture (Strict Compliance)
* **No Plaintext Storage:** This plugin does **not** generate or use local plaintext configuration files (e.g., no `config.json`). 
* **Standard Environment Variables:** Authentication strictly relies on standard MCP environment variables to ensure your credentials remain secure.
* **Least Privilege & Withdrawals:** This SDK explicitly supports asset transfers and withdrawals. We **strongly recommend** that your API Keys have **Withdrawals Disabled** and are restricted to **Read/Trade only**. Always enforce **IP Whitelisting** in your ZKE API management console.
* **Local Build Only:** The included installer strictly builds local TypeScript/Python dependencies and registers the plugin. It does not fetch executable code from remote, unverified sources during runtime.

---

## 🛠️ Installation & Setup

1. **Compile & Register Plugin:**
   Run the bundled secure build script. This will set up the Python virtual environment and compile the local TypeScript bridge:
   ```bash
   bash install_openclaw_plugin.sh

2.Configure Environment Variables (Required):
You must provide the following environment variables in your OpenClaw host configuration to enable trading capabilities:

ZKE_API_KEY: Your ZKE API Access Key

ZKE_SECRET_KEY: Your ZKE API Secret Key

🪄 Magic Prompts
"What is the current market depth for ASTER/USDT?"

"Place a limit sell order for 10 ASTER at 0.85."

"Transfer 100 USDT from my Spot account to my Futures account."

"Show my recent trading history on ZKE."

🔗 Official Resources
Website: https://zke.com

Interactive Guide: https://support.zke.com/skills/

GitHub Repository: https://github.com/ZKE-Exchange/zke-trading-sdk

Licensed under MIT-0. Developed by ZKE Exchange AI Division.