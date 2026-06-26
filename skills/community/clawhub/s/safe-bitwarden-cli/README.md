# Safe Bitwarden CLI (Agent Skill)

[简体中文](./README_zh.md)

An industrial-grade, secure, and conversational bridge for Bitwarden Vault. 

## Key Philosophy: AI Password Blindness
This skill implements a **Native Clipboard Proxy** pattern. It allows an AI agent to search your vault and trigger a copy event, but the **plain passwords never enter the AI's context, logs, or memory**. 

### How it works:
1. **Search**: The agent retrieves only non-sensitive metadata (Item Name, ID, Username).
2. **Transfer**: When you ask the agent to "copy the password", it executes a direct OS-level pipe: `bw get password $ID | pbcopy`.
3. **Isolation**: The secret flows directly from Bitwarden to your system clipboard via the kernel. 

## Audit-Perfect Security (v1.5.1)
- **Pure Shell**: Implemented in Bash to avoid high-level runtime subprocess vulnerabilities.
- **Zero Eval**: All native tools are called directly without shell interpolation risks.
- **Zero Dependencies**: Uses only native tools (`bw`, `pbcopy`/`clip`, `python3`) already present on most systems.

## Installation & Setup

1. **Requirements**:
   - [Bitwarden CLI (`bw`)](https://github.com/bitwarden/clients/tree/master/apps/cli)
   - Python 3 (standard on macOS/Linux)

2. **Environment Variable**:
   You must export your session token locally. The skill **cannot** and **will not** prompt for your master password.
   ```bash
   export BW_SESSION=$(bw unlock --raw)
   ```

3. **Verify**:
   ```bash
   bash scripts/main.sh setup
   ```

## Usage

- **Agent**: "I've searched your Bitwarden vault for 'Gmail'. I found an account with username 'user@gmail.com'. Would you like me to copy the password to your clipboard?"
- **User**: "Yes, please."
- **Agent**: (Executes `copy` action) "Done. The password is now in your native clipboard."

## Registry Metadata (ClawHub)
This skill is optimized for high-trust registries like ClawHub. It explicitly declares all required binaries and environment variables.
