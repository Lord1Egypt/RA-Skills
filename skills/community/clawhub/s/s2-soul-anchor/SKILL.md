# ⚓ S2-Soul-Anchor: Deterministic Identity Anchor

This SKILL safely generates a baseline `SOUL.md` template and calculates a mathematically permanent offline **S2-DID** (Decentralized Identifier) for your local Openclaw agent.

### 🛡️ Why it's 100% Safe and Reliable
- **Deterministic**: Unlike random generators, this tool uses a SHA-256 hash of your Agent's Name. If your agent is named "CyberCrayfish", it will always generate the exact same permanent DID.
- **100% Local**: Zero network calls. No API keys required. 
- **Read-Only (HITL)**: Outputs directly to the console for Human-In-The-Loop safe copying. It will NOT overwrite your files automatically.

### ⚙️ Usage
1. Run the skill locally.
2. Copy the generated `SOUL.md` template (which includes your deterministic `S2-DID`) from the terminal.
3. Paste it into your local workspace. 

*Optional: Want a public Web3 dossier or a physical Matrix Coordinate? Take your generated S2-DID and register it manually on the [Space2.world](https://space2.world) global matrix!*