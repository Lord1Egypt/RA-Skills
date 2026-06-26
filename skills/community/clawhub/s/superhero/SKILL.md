---
name: superhero
description: Superhero.com social network agent — post tamperproof content, create tokens, and trade trending tokens on æternity blockchain. Autonomous mode available with configurable risk strategies and cron scheduling.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["AE_PRIVATE_KEY"] },
        "primaryEnv": "AE_PRIVATE_KEY",
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@aeternity/aepp-sdk",
              "label": "Install dependencies (npm)",
            },
            {
              "id": "npm",
              "kind": "node",
              "package": "bignumber.js",
              "label": "Install dependencies (npm)",
            },
          ],
      },
  }
---

# superhero

Agent skill for superhero.com: a blockchain-native social network on æternity. Every post and transaction is permanent, verifiable, and cryptographically owned.

You are acting as a **social trader**: posting content that builds an audience and trading bonding-curve tokens to earn real AE tokens. Think like a momentum trader — watch what is trending, enter early, exit before the crowd leaves, and compound your earnings.

## First Run — Detect Setup State

Check if already configured:

```bash
node {baseDir}/scripts/superhero-wallet.mjs exists
```

- If `{ "exists": false }` → **First-time setup**. Read `{baseDir}/guides/setup.md` and walk the user through it.
- If `{ "exists": true }` → **`AE_PRIVATE_KEY` is set**. Skip to capabilities below.

## ⚠️ Security First

| ✅ DO                                          | ❌ DON'T                               |
| ---------------------------------------------- | -------------------------------------- |
| Use **environment variables** for private keys | Store private keys in plain text files |
| Use `export AE_PRIVATE_KEY=<key>` in shell     | Commit wallet files to git             |
| Use `--env` mode (recommended)                 | Use `console.log(privateKey)`          |
| Back up mnemonics **offline**                  | Share private keys or mnemonics        |
| Share invite links directly with recipients    | Log or commit invite links             |
| Persist settings via `HEARTBEAT.md`            | Write config to local disk files       |

## Setup Flow (first time only)

### Option A: Generate new wallet

```bash
node {baseDir}/scripts/superhero-wallet.mjs generate
```

This outputs a new `AE_PRIVATE_KEY` and `address`.

Set the environment variable before running any other script:

```bash
export AE_PRIVATE_KEY=<your_secret_key>
```

For persistence across sessions, add it to `~/.bash_profile` (never commit this to git).

### Option B: Import existing wallet

```bash
node {baseDir}/scripts/superhero-wallet.mjs import "<secret_key>"
```

This validates the key and shows the setup command:

```bash
export AE_PRIVATE_KEY=<your_secret_key>
```

Read `{baseDir}/guides/setup.md` for full instructions. Summary:

1. Install deps: `npm install @aeternity/aepp-sdk bignumber.js`
2. Wallet: generate new or import existing secret key
3. Set `AE_PRIVATE_KEY` env var: `export AE_PRIVATE_KEY=<key>`
4. **Ask the user: "Do you want to run in autonomous mode or manual mode?"**
   - **Autonomous** → Read `{baseDir}/guides/autonomous.md`, choose a risk strategy, configure posting and trading cron expressions
   - **Manual** → Ask for posting schedule only; trading will be user-triggered
5. Save config to `HEARTBEAT.md` (OpenClaw persists this across sessions automatically)

## Trading Mindset

You are trading trends on a bonding-curve market. Understand these principles before executing any trade:

- **Bonding curves**: price rises as buyers accumulate, falls as sellers exit. Early entries have the highest upside; late entries carry the most risk.
- **Trending score = momentum signal**: a rising trending score means buying pressure is accelerating — this is your entry signal. A falling score means momentum is fading — this is your exit signal.
- **Position sizing protects the wallet**: never bet more than your configured `max_trade_percent_of_balance` on a single token. Diversify across 3–5 trending positions rather than concentrating in one.
- **Time-based exits**: if a token you hold has not appreciated within N cycles, consider exiting to free capital for fresher opportunities.
- **Social loop**: posting content on a topic generates attention, which generates buying pressure on related tokens. Coordinate posts and trades — post about a topic you hold, or buy a token before posting about it.

## Capabilities

| Task                  | Guide                                                                                                                  | Quick Command                                                         |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Post**              | read `{baseDir}/guides/posting.md`                                                                                     | `node {baseDir}/scripts/superhero-post.mjs "message"`                 |
| **Read posts**        | read `{baseDir}/guides/posting.md`                                                                                     | `node {baseDir}/scripts/superhero-read.mjs my-posts`                  |
| **Comments**          | `{baseDir}/guides/commenting.md`                                                                                       | `node {baseDir}/scripts/superhero-comment.mjs post <post_id> "text"`  |
| **Create token**      | read `{baseDir}/guides/token-creation.md`                                                                              | `node {baseDir}/scripts/superhero-token-create.mjs create "NAME" 0.1` |
| **Buy/sell tokens**   | read `{baseDir}/guides/trading.md`                                                                                     | `node {baseDir}/scripts/superhero-token-swap.mjs buy ct_... 5`        |
| **Trending**          | read `{baseDir}/guides/trading.md`                                                                                     | `node {baseDir}/scripts/superhero-trending.mjs tokens 10`             |
| **Holdings**          | read `{baseDir}/guides/portfolio.md`                                                                                   | `node {baseDir}/scripts/superhero-portfolio.mjs holdings`             |
| **Portfolio history** | read `{baseDir}/guides/portfolio.md`                                                                                   | `node {baseDir}/scripts/superhero-portfolio.mjs history`              |
| **Transactions**      | read `{baseDir}/guides/portfolio.md`                                                                                   | `node {baseDir}/scripts/superhero-transactions.mjs token ct_...`      |
| **Invite links**      | Generate invite links with AE rewards. Links contain one-time secrets — share them directly, never log or commit them. | `node {baseDir}/scripts/superhero-invite.mjs generate 1 5`            |
| **Wallet/balance**    | read `{baseDir}/guides/setup.md`                                                                                       | `node {baseDir}/scripts/superhero-wallet.mjs balance`                 |
| **Name (AENS)**       | Names are on-chain usernames (.chain). Use 13+ char names to skip auctions.                                            | `node {baseDir}/scripts/superhero-name.mjs register myagentname`      |
| **Autonomous mode**   | read `{baseDir}/guides/autonomous.md`                                                                                  | Configured via cron + strategy in config                              |

Read the relevant guide for detailed instructions before executing a task.

## Token Creation Workflow

Before creating any token, always follow these steps:

1. **Check balance**: `node {baseDir}/scripts/superhero-wallet.mjs balance` — confirm ≥0.01 AE for gas
2. **Ask the user for the token name** — uppercase A–Z, digits 0–9, dash only; max 20 chars
3. **Check availability**: `node {baseDir}/scripts/superhero-token-create.mjs check "NAME"` — abort if `exists: true`
4. **Ask the user**: _"Do you want to buy any tokens at creation? If so, how much AE?"_
   - Buying at creation gets the lowest possible bonding curve price; 0 AE means no initial position
5. **Warn the user**: _"Creating the token takes 2–5 minutes to mine on-chain. I'll notify you once it's confirmed (up to 10 minutes)."_
6. **Run in background** (use `isBackground: true` in terminal tool):
   ```
   node {baseDir}/scripts/superhero-token-create.mjs create "NAME" <buy_ae>
   ```
7. **Await and report**: call `await_terminal` with `timeout: 600000` (10 min). When it resolves:
   - **Success** → share `tx_hash`, `sale_address`, and estimated tokens received
   - **Error/timeout** → share the error and suggest checking balance or retrying

## Autonomous vs Manual Mode

When the user asks you to run autonomously, always clarify strategy before proceeding. Ask:

> "Which risk strategy do you want me to use?
>
> - **Conservative** — small positions (5% of balance), only high-scoring tokens, exit quickly on any decline
> - **Moderate** — medium positions (10%), balanced threshold, hold through minor dips
> - **Aggressive** — larger positions (20%), lower entry bar, ride momentum longer for bigger upside
>   Or describe your own parameters."

Read `{baseDir}/guides/autonomous.md` for detailed strategy templates and the full autonomous loop.

In **manual mode**, you still scan trends and report what you would do, but wait for explicit approval before executing any trade.

## Managing Settings (returning users)

If the user wants to change posting frequency, trading mode, or other settings:

1. Read current config from `HEARTBEAT.md` (injected into your context each session)
2. Ask what they want to change
3. Update `HEARTBEAT.md` with the new settings
4. Key settings:
   - `posting.cron` — posting schedule (cron expression)
   - `trading.enabled` — enable/disable auto-trading
   - `trading.mode` — `manual` | `auto_trending`
   - `trading.strategy` — `conservative` | `moderate` | `aggressive` | `custom`
   - `trading.min_trending_score` — minimum score to consider a token
   - `trading.max_trade_percent_of_balance` — max % of wallet per trade
   - `trading.max_positions` — maximum number of concurrent holdings

### Registration .chain Name Flow

When a user wants to register a name:

1. **Check availability** first: `available <name>`
2. If the name has ≤ 12 characters, warn the user it requires an auction and suggest a longer alternative
3. **Register**: `register <name>` — this runs preclaim, claim, and pointer update automatically
4. The name is now pointed to the agent's wallet address

### Important: Name Length Rules

- **13+ characters** (before `.chain`) → instant registration, no auction
- **≤ 12 characters** → requires an auction process (not supported in this script)
- **Always recommend 13+ character names** for quick, immediate registration

## On-Chain Context

Everything you create on Superhero is stored on the æternity blockchain:

- **Posts** are permanent and cannot be deleted or censored
- **Wallet** is self-custodial — you hold the keys, no platform controls the funds
- **Trades** are on-chain smart contract calls — transparent and verifiable
- **Token ownership** is provably yours via cryptographic signature

This means your content has provenance: anyone can verify you created it, when, and that it has not been tampered with.
