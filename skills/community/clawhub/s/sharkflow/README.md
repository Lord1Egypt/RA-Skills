# ⚡ SharkFlow

**On-Chain Task Automation** - Automate your DeFi workflows with task queues and multisig support!

[![Version](https://img.shields.io/github/v/release/gztanht/sharkflow)](https://github.com/gztanht/sharkflow/releases)
[![License](https://img.shields.io/github/license/gztanht/sharkflow)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-sharkflow-blue)](https://clawhub.com/skills/sharkflow)

> **Automate Your On-Chain Workflow** - Execute tasks like a shark! ⚡

---

## 🌟 Features

- **Task Queues** - Batch multiple on-chain operations
- **Multisig Support** - Safe/multi-signature wallet workflows
- **Scheduled Tasks** - Auto-execute at set times (DCA, auto-compound)
- **History Tracking** - Complete task execution logs
- **Completion Alerts** - Telegram/email notifications
- **Template System** - Save reusable operation templates
- **Dry-Run Mode** - Preview before submitting

---

## 🚀 Quick Start

```bash
# Install
npx @gztanht/sharkflow

# Add deposit task
node scripts/flow.mjs add --action deposit --token USDT --amount 1000 --platform aave

# Add swap task
node scripts/flow.mjs add --action swap --from ETH --to USDC --amount 0.5

# Execute all queued tasks
node scripts/flow.mjs execute

# Set weekly DCA schedule
node scripts/flow.mjs schedule --action deposit --amount 100 --recur weekly --day monday
```

---

## 📊 Use Cases

### 💰 Yield Farming Automation

```bash
# Queue: Deposit → Stake → Compound
node scripts/flow.mjs add --action deposit --token USDC --amount 5000 --platform aave
node scripts/flow.mjs add --action stake --amount 5000 --platform aave
node scripts/flow.mjs schedule --action compound --recur weekly
node scripts/flow.mjs execute
```

### 🔐 Multisig Treasury Management

```bash
# Create multisig task
node scripts/flow.mjs multisig create --required 3 --signers 0x123,0x456,0x789

# Sign task
node scripts/flow.mjs multisig sign --taskId 123

# Check status
node scripts/flow.mjs multisig status --taskId 123
```

---

## 💰 Pricing - Free First!

| Plan | Price | Limit |
|------|-------|-------|
| **Free** | $0 | **5 tasks/day** |
| **Sponsor Unlock** | 0.5 USDT or 0.5 USDC | Unlimited |

### Sponsorship Addresses

- **USDT (ERC20)**: `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- **USDC (ERC20)**: `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

---

## 📖 All Commands

| Command | Description |
|---------|-------------|
| `flow.mjs add` | Add task to queue |
| `flow.mjs execute` | Execute queued tasks |
| `flow.mjs execute --dry-run` | Preview without submitting |
| `flow.mjs schedule` | Set scheduled task |
| `flow.mjs schedule --list` | List all schedules |
| `flow.mjs multisig create` | Create multisig task |
| `flow.mjs multisig sign` | Sign a task |
| `flow.mjs multisig status` | Check signature status |

---

## 🔄 Supported Actions

| Action | Description | Platforms |
|--------|-------------|-----------|
| `deposit` | Deposit to protocol | Aave, Compound, Spark |
| `withdraw` | Withdraw from protocol | Aave, Compound, Spark |
| `swap` | Token swap | Uniswap, Curve, 1inch |
| `stake` | Stake tokens | Lido, Rocket Pool |
| `claim` | Claim rewards | All yield platforms |
| `bridge` | Cross-chain bridge | Stargate, Hop, Across |

---

## 🛡️ Safety Features

- ✅ **Dry-Run Mode** - Preview results before submitting
- ✅ **Transaction Limits** - Set per-tx/daily limits
- ✅ **Contract Whitelist** - Only allow predefined contracts
- ✅ **Multisig Confirmation** - Large transactions require multiple signatures

---

## 🔧 Configuration

Edit `config/wallets.json` to add wallets:

```json
{
  "wallets": [
    {"name": "Main", "address": "0x...", "type": "EOA"},
    {"name": "Safe", "address": "0x...", "type": "Safe", "required": 2, "signers": [...]}
  ]
}
```

---

## 📈 Roadmap

- **v0.1.x** ✅ Framework release
- **v0.2.0** ⏳ Wallet integration
- **v0.3.0** ⏳ Smart contract execution
- **v0.4.0** ⏳ Telegram notifications
- **v1.0.0** ⏳ Full automation suite

---

## ⚠️ Security Warning

- ⚠️ Smart contract interactions carry risk
- ⚠️ Always verify transaction details before signing
- ⚠️ Use hardware wallets for large amounts
- ⚠️ This tool provides automation only, not financial advice

**Never share your private keys!**

---

## 📞 Support

- **ClawHub**: https://clawhub.com/skills/sharkflow
- **Email**: support@sharkflow.shark
- **Telegram**: @SharkFlowBot

---

## 📄 License

MIT © 2026 gztanht

---

**Made with ⚡ by [@gztanht](https://github.com/gztanht)**

*Automate Your On-Chain Workflow!*
