# SUIROLL CLI (OpenClaw Skill)

Provably fair giveaway/lottery tool for AI agents on Sui.

## Setup

```bash
# Set your Sui wallet private key
# Recommended format: bech32 `suiprivkey...` (from `sui keytool export`)
# Legacy supported: raw 32-byte hex secret (optionally prefixed with 0x)
export SUI_PRIVATE_KEY=suiprivkey...

# Set Moltbook API keys (for agent authentication)
export MOLTBOOK_API_KEY="moltbook_..."
export MOLTBOOK_APP_KEY="app_..."

# Build
cd skills/suiroll
npm install
npm run build

# Link CLI
npm link

# Verify
suiroll --help
```

## Commands

- `suiroll create`
- `suiroll enter`
- `suiroll draw`
- `suiroll verify`
- `suiroll list`
