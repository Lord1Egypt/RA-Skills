# Relay Link Bridge Skill (Full Documentation)

This folder contains the complete implementation of the **Relay Link Bridge** skill for OpenClaw.

## 🚀 Key Features
- **Automated Execution:** Sign and send bridge transactions from Avalanche automatically using `cast` (Foundry).
- **Dynamic Config:** Automatically reads Private Keys and Wallet Addresses from `~/.openclaw/config.env`.
- **User Friendly:** Supports natural language commands like "bridge 0.02 avax to sol".
- **Smart Tracking:** Intelligent status tracking that resolves transaction hashes to Request IDs for accurate monitoring.

## 📁 Folder Structure
- `SKILL.md`: Core instructions for the AI agent.
- `scripts/quick-bridge.sh`: The main execution engine for bridging.
- `scripts/get-status.sh`: Intelligent transaction status tracker.
- `scripts/get-chains.sh`: Helper to list supported blockchains.
- `scripts/get-tokens.sh`: Helper to list supported tokens.

## 🛠️ Installation Guide
1. Copy this `RelaySKILL` folder to `~/.openclaw/skills/relay-link/`.
2. Ensure your Private Key and Addresses are set in `~/.openclaw/config.env`:
   ```bash
   AVAX_PRIVATE_KEY=your_key_here
   EVM_ADDRESS=your_address_here
   SOLANA_ADDRESS=your_solana_address_here
   ```
3. Grant execution permissions:
   ```bash
   chmod +x scripts/*.sh
   ```

## 📝 Example Commands
- "bridge 0.02 avax to sol"
- "check status for bridge [hash]"
- "list all supported chains"

---
*Created by Gemini CLI - March 28, 2026*
