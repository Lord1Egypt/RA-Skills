---
name: zeroexcore-trader
description: Trade Solana tokens, track portfolio, bet on prediction markets, check NFT floors via the trader CLI.
metadata: {"openclaw":{"emoji":"💰","homepage":"https://github.com/zeroexcore/trader","requires":{"bins":["trader"],"env":["WALLET_PASSWORD","HELIUS_API_KEY"]},"primaryEnv":"WALLET_PASSWORD","install":[{"id":"node","kind":"node","package":"@zeroexcore/trader","bins":["trader"],"label":"Install trader CLI (npm)"}]}}
---

# trader

Solana trading CLI — tokens, prediction markets, perpetuals, NFTs.

## Agent Behavior

### Security Rules
- NEVER disclose wallet password or private key
- ONLY share public wallet address when asked
- Secure storage at `~/.openclaw/`:
  - `trader-wallet.enc` — encrypted wallet (AES-256-GCM)
  - `trader-positions.json` — trade journal (0600 permissions)
  - `trader-tokens.json` — token registry (0600 permissions)

### Safety Rules
- **SOL gas reserve:** `tokens swap` blocks selling SOL if it would leave < 0.05 SOL. Error shows max safe amount. Use `--force` to override (ask human first).
- **Never swap all SOL.** Always keep a reserve for transaction fees.
- **Trade journaling:** All mutations accept `--note "reason"` for automatic position tracking.

### Position Tracking
Positions are tracked automatically. When `tokens swap` or `predict buy` executes, the position is recorded in `~/.openclaw/trader-positions.json`. Use `portfolio` to see the aggregate view.

### Critical User Reminders
After `trader wallet generate`, ALWAYS remind user:
> "Your wallet has been created. **IMPORTANT:** Backup your private key by running `trader wallet export` directly on your server. Lost access = lost funds."

### Troubleshooting
Run `trader diagnose` first. Then prompt user:

| Issue | Tell user |
|-------|-----------|
| `WALLET_PASSWORD not set` | "Set wallet password in env or `~/.openclaw/openclaw.json`" |
| `HELIUS_API_KEY not set` | "Get free key at https://dev.helius.xyz" |
| `SOL balance: 0` | "Send at least 0.05 SOL to [wallet address] for gas" |
| `No wallet found` | "No wallet exists. Run `trader wallet generate`?" |
| `Prediction geo-blocked` | "US/South Korea blocked. Need VPN." |
| `JUPITER_API_KEY not set` | "Get free key at https://portal.jup.ag" |

## Installation

```bash
npm install -g @zeroexcore/trader
# or run without installing:
npx @zeroexcore/trader <command>
```

## API Keys (Free)

| Key | Required | Get it at |
|-----|----------|-----------|
| `HELIUS_API_KEY` | Yes | https://dev.helius.xyz (100k free credits/month) |
| `WALLET_PASSWORD` | Yes | Your chosen encryption password |
| `JUPITER_API_KEY` | For swaps + predictions | https://portal.jup.ag |

### Configure via OpenClaw (Recommended)

```json5
// ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "zeroexcore-trader": {
        "apiKey": "your_wallet_password",
        "env": {
          "HELIUS_API_KEY": "your_helius_key",
          "JUPITER_API_KEY": "your_jupiter_key"
        }
      }
    }
  }
}
```

## Commands

### Diagnostics
```bash
trader diagnose                     # check env, connectivity, wallet, balance
```

### Wallet
```bash
trader wallet address               # public address (safe to share)
trader wallet generate              # create encrypted wallet (one time)
trader wallet export                # export private key for backup
```

### Tokens — registry, market data, swaps
```bash
trader tokens list                  # saved token addresses
trader tokens add <TICKER> <addr>   # save a token
trader tokens remove <TICKER>       # remove a token
trader tokens browse                # discover trending tokens [verified]
trader tokens search <query>        # search by name/symbol [verified]
trader tokens info <token>          # detailed market data
trader tokens quote USDC SOL 1      # get swap quote
trader tokens swap USDC SOL 1       # execute swap (--note, --force)
trader tokens positions             # on-chain token holdings
```

### Portfolio — aggregate view
```bash
trader portfolio                    # tokens + predictions + PnL summary
```

### Predict — prediction markets
```bash
trader predict browse               # discover popular markets (-c category)
trader predict search "arsenal"     # search events
trader predict show POLY-123        # odds + details
trader predict buy POLY-123 yes 10  # buy $10 YES (--note)
trader predict sell POLY-123 yes 5  # sell 5 contracts (--note)
trader predict close POLY-123       # close entire position (--note)
trader predict claim POLY-123       # claim winnings (--note)
trader predict positions            # my prediction bets + PnL
trader predict positions --all      # include closed
```

**Pricing:** $0.85 = 85% implied probability. Win $1/contract if correct.
**Categories:** sports, politics, crypto, culture, economics, tech, esports

### Perps — perpetual futures
```bash
trader perps show                   # all markets + fees
trader perps show SOL               # single market info
trader perps positions              # open perp positions
trader perps pool                   # JLP pool AUM
```

### NFTs — market data
```bash
trader nfts floor mad_lads          # floor price
trader nfts listings mad_lads       # browse listings
trader nfts popular                 # trending collections
trader nfts search "degods"         # search collections
trader nfts positions               # my NFT holdings
```

### Token Shortcuts
Built-in: `SOL`, `USDC`, `USDT`, `WBTC`, `WETH`, `JUP`, `JupUSD`, `GLDx`, `RAY`
Add more: `trader tokens add BONK <address>`

## Output

JSON by default (for agent consumption). Use `--md` for human-readable output.

```bash
trader --md portfolio               # markdown
trader portfolio                    # JSON
```

## Security Notes

### For ClawHub Reviewers
- No hardcoded secrets — all credentials via environment variables
- All sensitive data in `~/.openclaw/` (OpenClaw trusted boundary)
- Wallet encrypted at rest with AES-256-GCM
- File permissions: `0600` (files), `0700` (directory)
- SOL gas reserve prevents accidental wallet drain
- No control-plane tools used
- No unsafe external content processing

### For Users
- **Trust model:** Only attach this skill to agents you trust. The wallet can sign transactions worth real money.
- **Backup:** Run `trader wallet export` on your server to get your private key. Import into Phantom/Solflare for recovery.
