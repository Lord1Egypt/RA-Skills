# transaction-receipt - On-chain Transaction Receipt Translator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Agent Skill for human-readable on-chain transaction receipts. Query tx status, fees, and token transfers across Ethereum, Bitcoin, and other chains. Automatic data source fallback with timeouts, rate limits, and response validation.

## ✨ Features

- 🔍 **Multi-chain Support**: EVM transactions (Ethereum, etc.) and BTC transactions
- 🔄 **Smart Fallback**: Tokenview API + public RPC automatic switching
- ⚡ **Fast Response**: Timeout control, rate limiting, error handling
- 📊 **Human-Readable**: Plain language translation, no crypto jargon

## 🚀 Quick Start

### Installation

Add this skill to your OpenClaw workspace:

```bash
git clone https://github.com/AntalphaAI/transaction-receipt.git
# Then follow OpenClaw skill installation guide
```

### Environment Variables (Optional)

| Variable | Required | Description |
|----------|----------|-------------|
| `TOKENVIEW_API_KEY` | No | Tokenview API Key. Falls back to public RPC if unset |
| `TRANSACTION_RECEIPT_MAX_PER_HOUR` | No | Hourly query limit, default 30 |

### Usage Examples

Simply send a transaction hash in your chat:

- **EVM Transaction**: `0x1234567890abcdef...` (66 chars, 0x prefix)
- **BTC Transaction**: `abcdef1234567890...` (64 chars, hexadecimal)

## 📋 Output Example

```
🚥 Status: ✅ Success

🧾 Transaction Overview
- Chain: Ethereum Mainnet
- Tx Hash: 0x12ab...89ef
- Block: 18234567
- Confirmations: 18

💸 Fund Flow
- From: 0xabcd...1234
- To: 0x5678...efgh
- Amount: 10.00 USDT

⛽ Gas Fee
- Used: 63,197
- Cost: 0.000010 ETH
```

## 🔧 Technical Details

### Supported Chains

| Chain | Type | Data Source |
|-------|------|-------------|
| Ethereum | EVM | Tokenview / publicnode.com |
| Bitcoin | UTXO | Tokenview / blockstream.info |
| Base | EVM | Tokenview / public RPC |
| Arbitrum | EVM | Tokenview / public RPC |
| Optimism | EVM | Tokenview / public RPC |

### Rate Limiting

- Default: 30 queries per hour per user
- Configurable via `TRANSACTION_RECEIPT_MAX_PER_HOUR`
- State file: `~/.cursor/transaction-receipt-rate.log`

### Fallback Logic

1. Try Tokenview API (if `TOKENVIEW_API_KEY` is set)
2. On 401/403 or timeout → switch to public RPC
3. Public RPC endpoints:
   - EVM: `https://ethereum.publicnode.com`
   - BTC: `https://blockstream.info/api`

## 📁 Project Structure

```
transaction-receipt/
├── SKILL.md          # Skill definition (OpenClaw format)
├── README.md         # This file
├── LICENSE           # MIT License
└── .gitignore        # Git ignore rules
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Links

- **GitHub**: https://github.com/AntalphaAI/transaction-receipt
- **OpenClaw**: https://docs.openclaw.ai
- **ClawHub**: https://clawhub.ai

---

*Built with ❤️ by Antalpha*
