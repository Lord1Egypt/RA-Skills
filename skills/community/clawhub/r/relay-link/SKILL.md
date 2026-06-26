---
name: relay-link
description: "Professional Bridge & Swap skill using Relay.link. Supports automated execution and smart tracking for 70+ networks."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔀",
        "requires": { 
          "bins": ["curl", "jq", "cast", "bc"],
          "env": ["EVM_PRIVATE_KEY", "EVM_ADDRESS", "SOLANA_ADDRESS"]
        },
      },
  }
---

# Relay Master Skill (v1.1.0)

Professional token bridging and intelligent transaction tracking across **70+ blockchain networks**.

## 🛠 Prerequisites
Ensure \`~/.openclaw/config.env\` contains:
- \`EVM_PRIVATE_KEY\`: For signing transactions.
- \`EVM_ADDRESS\`: Your sender wallet address.
- \`SOLANA_ADDRESS\`: Your default Solana recipient address.

## 🚀 Commands

### 1. Bridge Tokens
**Trigger:** "bridge [amount] [from] to [to]"
**Action:**
\`\`\`~/.openclaw/skills/relay-link/scripts/quick-bridge.sh [amount] [from] [to]\`\`\`

### 2. Check Status
**Trigger:** "status [hash_or_id]"
**Action:**
\`\`\`~/.openclaw/skills/relay-link/scripts/get-status.sh [hash_or_id] [from_chain]\`\`\`

### 3. Network List
**Trigger:** "list chains" or "tokens"
**Action:**
\`\`\`~/.openclaw/skills/relay-link/scripts/get-chains.sh\`\`\`

---

## 📋 Major Networks
- **Major:** eth (1), base (8453), op (10), arb (42161), avax (43114), sol (792703809), poly (137), bsc (56)
- **Emerging:** abstract, bera, hl, monad, sonic, story, unichain.

## ⚠️ AI Safety Rules
1. **Always Quote & Confirm:** You MUST show the quote summary (estimated receive amount and fees) and wait for the user to say "yes" before executing any transaction.
2. **Auto-Auth:** Scripts handle credentials automatically from \`config.env\`.
3. **Transparent Execution:** Inform the user that bridge transactions typically take 1-3 minutes to finalize.
