# Unclaimed SOL Scanner

Scan any Solana wallet for reclaimable SOL locked in dormant token accounts and program buffer accounts — from any AI assistant.

Powered by [Unclaimed SOL](https://unclaimedsol.com).

## Install

**OpenClaw / ClawHub:**
```bash
clawhub install unclaimed-sol-scanner
```

**Or paste this repo URL into OpenClaw** and it will let you choose to install.

**Manual:**
```bash
cp -r unclaimed-sol-scanner ~/.openclaw/skills/
```

## What it does

Every token interaction on Solana creates an account with rent locked in it. Dead memecoins, old NFTs, forgotten airdrops — they all leave rent behind. This skill scans any wallet and tells you how much SOL is reclaimable.

**Example:**
> You: "Scan this wallet for unclaimed SOL: 7xKXq1..."
>
> Agent: "Your wallet has 4.728391 SOL reclaimable across 186 accounts."

## Read-only

This skill only scans. It does not execute transactions, ask for private keys, or modify your wallet in any way.

To claim your SOL, visit [unclaimedsol.com](https://unclaimedsol.com).

## Privacy & Data Disclosure

**This skill sends the user's Solana public wallet address to the Unclaimed SOL API** (`https://unclaimedsol.com/api/check-claimable-sol`) via an HTTPS POST request to check for reclaimable SOL. This is the only data transmitted.

- No private keys, seed phrases, or signing capabilities are involved.
- The agent is instructed to **inform the user and obtain consent** before making the API call.
- See the [Unclaimed SOL Privacy Policy](https://blog.unclaimedsol.com/privacy-policy/) for how the API handles submitted addresses.

## Compatibility

Works with any tool that supports the [AgentSkills](https://docs.anthropic.com) format:
- OpenClaw
- Claude Code
- Cursor
- Any AgentSkills-compatible agent

## Security

- Read-only — no transactions, no signing
- No private keys or seed phrases required
- Uses only public blockchain data via the Unclaimed SOL API
- Agent must disclose and get user consent before transmitting wallet address

## Links

- [Unclaimed SOL](https://unclaimedsol.com) — claim your SOL
- [Privacy Policy](https://blog.unclaimedsol.com/privacy-policy/)
- [ClawHub](https://clawhub.ai) — browse OpenClaw skills

## Author

[Unclaimed SOL](https://unclaimedsol.com)

## License

MIT
