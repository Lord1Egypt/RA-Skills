# QFC OpenClaw Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-qfc-blue)](https://clawhub.ai/lai3d/qfc)

AI agent skill for interacting with the QFC blockchain. Provides wallet management, chain queries, staking info, and more — with built-in security policies.

## Install

```bash
# OpenClaw native
openclaw skills add https://github.com/qfc-network/qfc-openclaw-skill

# or via ClawHub
clawhub install qfc

# or without installing clawhub globally:
npx clawhub@latest install qfc
```

> **Tip:** To use `clawhub` directly, install it globally: `npm install -g clawhub`

## Update

```bash
# via ClawHub
clawhub update qfc
# or: npx clawhub@latest update qfc

# or if installed via openclaw skills add
cd ~/.openclaw/skills/qfc-openclaw-skill
git pull && npm install && npm run build
```

## Install from Source

```bash
git clone https://github.com/qfc-network/qfc-openclaw-skill.git
cd qfc-openclaw-skill
npm install && npm run build
```

## Features

### Wallet
- Create / import wallets (HD, private key)
- Balance queries & QFC transfers
- Message signing

### Wallet Persistence
- AES-encrypted keystore on disk (`~/.openclaw/qfc-wallets/`)
- Save, load, list, remove, and export keystore JSON
- Compatible with MetaMask / Geth keystore format

### Chain Queries
- Block, transaction, and receipt lookups

### Network & Validators
- Node info, network state, gas price
- Validator list with contribution scores & score breakdown

### Epoch & Finality
- Current epoch info, finalized block height

### ERC-20 Tokens
- **Deploy new tokens** — create ERC-20 tokens with one command (no compiler needed)
- Get token info (name, symbol, decimals, totalSupply)
- Check token balances, transfer tokens, approve spenders
- Auto-handles decimal conversion

### Smart Contracts
- Read contract state (call), write transactions (send), deploy contracts
- Check if an address is a contract, retrieve bytecode

### AI Inference
- Submit public inference tasks to QFC's decentralized GPU network
- Query approved models, estimate fees, wait for results
- Decode base64 result payloads from completed tasks
- Network-wide inference statistics (tasks, miners, FLOPS, pass rate)

### Faucet
- Request test QFC on testnet (chain_id=9000)

### Security
- Pre-transaction checks (amount limits, address validation, daily caps)
- Private keys / mnemonics never exposed in output

## Modules

| Module | Class | Description |
|--------|-------|-------------|
| `wallet` | `QFCWallet` | Create/import/balance/send/sign/save/load |
| `keystore` | `QFCKeystore` | Encrypted wallet persistence (scrypt KDF) |
| `security` | `SecurityPolicy` | Pre-transaction safety checks |
| `faucet` | `QFCFaucet` | Testnet token requests |
| `chain` | `QFCChain` | Block, transaction, receipt queries |
| `network` | `QFCNetwork` | Node info & network status |
| `staking` | `QFCStaking` | Validator & staking info |
| `epoch` | `QFCEpoch` | Epoch & finality info |
| `inference` | `QFCInference` | AI inference task submission & results |
| `contract` | `QFCContract` | Read/write/deploy smart contracts |
| `token` | `QFCToken` | ERC-20 token operations |
| `provider` | — | Shared provider creation & RPC helper |

## Network Configuration

Edit `config/qfc-networks.json` to customize RPC endpoints.

| Network | Chain ID | RPC |
|---------|----------|-----|
| Testnet | 9000 | https://rpc.testnet.qfc.network |
| Mainnet | 9001 | https://rpc.qfc.network |

## Usage Examples

Once installed, just tell your AI agent what you want in natural language:

### Wallet

```
Create a new QFC wallet on testnet
```

```
Show my wallet balance
```

```
Save my wallet with password "s3cret"
```

```
List my saved wallets
```

```
Load wallet 0x1234...abcd with password "s3cret"
```

### Faucet & Transfers

```
Request test QFC from the faucet
```

```
Send 5 QFC to 0xabcd...1234
```

### Chain Queries

```
What's the latest block number?
```

```
Look up transaction 0xabc123...
```

```
Show me block 1500 details
```

### Network & Validators

```
Show QFC testnet status
```

```
List all validators and their contribution scores
```

```
What's the score breakdown for validator 0x8d1d...?
```

### ERC-20 Tokens

```
Create a token called "My Token" with symbol MTK and 1 million supply on QFC testnet
```

```
What is the token at 0xabcd...?
```

```
Check my balance for token 0xabcd...
```

### Smart Contracts

```
Read the name() of ERC-20 contract 0xabcd...
```

```
Is 0x1234...abcd a contract?
```

### AI Inference

```
What AI models are available on QFC?
```

```
How much does it cost to run a text embedding on QFC?
```

```
Submit an inference task using qfc-embed-small with input "Hello world" and max fee 0.1 QFC
```

### Epoch & Finality

```
What epoch are we in?
```

```
What's the latest finalized block?
```

## Reference

See [SKILL.md](./SKILL.md) for the full agent capability description and [references/](./references/) for detailed operation guides.
