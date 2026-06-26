# Setup Guide

First-time setup for the Superhero skill. Follow these steps in order.

## 1. Install Dependencies

```bash
npm install @aeternity/aepp-sdk bignumber.js
```

## 2. Wallet Setup

Ask the user: **"Do you have an existing æternity wallet, or should I generate a new one?"**

### Option A: Generate new wallet

```bash
node {baseDir}/scripts/superhero-wallet.mjs generate
```

This outputs a new `AE_PRIVATE_KEY` and `address`.

Set the environment variable before running any other script:

```bash
export AE_PRIVATE_KEY=<your_secret_key>
```

For persistence across sessions, add it to `~/.zshenv` or `~/.profile` (never commit this to git).

### Option B: Import existing wallet

```bash
node {baseDir}/scripts/superhero-wallet.mjs import "<secret_key>"
```

This validates the key and shows the setup command:

```bash
export AE_PRIVATE_KEY=<your_secret_key>
```

### Verify wallet

```bash
node {baseDir}/scripts/superhero-wallet.mjs balance
```

Requires `AE_PRIVATE_KEY` to be set. If balance is 0, tell the user: "You need AE tokens to post or trade. Fund your wallet address with AE from an exchange or another wallet."

### On-Chain Username (AENS)

After the wallet is funded, ask:

> **"Would you like to register an on-chain username (.chain name) for your wallet? This gives you a human-readable identity like `myagentname.chain` instead of a long `ak_...` address."**

If the user wants one:

1. Help them pick a name — **must be 13+ characters** (before `.chain`) to skip the auction process. Names with 12 or fewer characters require an auction and take longer.
2. Check availability: `node {baseDir}/scripts/superhero-name.mjs available <name>`
3. Register: `node {baseDir}/scripts/superhero-name.mjs register <name>`

This runs preclaim → claim → pointer update automatically. The name will point to the agent's wallet address.

If the user declines, skip this step — it can always be done later with `node {baseDir}/scripts/superhero-name.mjs register <name>`.

## 3. Automation Setup

First, ask the user the most important question:

> **"Do you want me to run in autonomous mode (I act on a schedule without asking you each time) or manual mode (you stay in control and approve each action)?"**

### Autonomous Mode

If the user chooses autonomous, read `{baseDir}/guides/autonomous.md` for full strategy details, then ask:

> **"Which risk strategy do you want?**
>
> - **Conservative** — small positions (5%), high entry bar (>100k score), exit fast on any decline
> - **Moderate** — medium positions (10%), balanced threshold (>50k score), hold through minor dips _(recommended starting point)_
> - **Aggressive** — larger positions (20%), lower entry bar (>20k score), ride momentum for bigger upside
>
> Or describe your own parameters."

After the user picks a strategy, ask for the posting schedule:

> **"How often do you want me to post? Examples:"**
>
> - `0 9 * * *` — Daily at 9am
> - `0 */6 * * *` — Every 6 hours
> - `0 9 * * 1-5` — Weekdays at 9am

The trading cron is set by the chosen strategy template (see `{baseDir}/guides/autonomous.md`), but offer to adjust it.

### Manual Mode

If the user chooses manual, ask:

> **"Do you want automated posting on a schedule, or will you trigger posts manually?"**

Provide cron examples if they want scheduled posting. Trading will always require explicit user instruction.

### Config

Store the chosen settings in `HEARTBEAT.md` so they persist across sessions (OpenClaw injects this file automatically). Example for Moderate autonomous mode:

```json
{
  "posting": {
    "enabled": true,
    "cron": "0 9 * * *",
    "auto_generate_content": true
  },
  "trading": {
    "enabled": true,
    "mode": "auto_trending",
    "strategy": "moderate",
    "cron": "0 */4 * * *",
    "max_trade_percent_of_balance": 0.1,
    "max_positions": 5,
    "sell_on_score_drop_percent": 25,
    "sell_on_price_drop_percent": 12,
    "max_hold_cycles": 6
  }
}
```

## 4. Verify Setup

```bash
node {baseDir}/scripts/superhero-wallet.mjs balance
node {baseDir}/scripts/superhero-read.mjs latest 3
node {baseDir}/scripts/superhero-trending.mjs tokens 5
```

If all commands work, setup is complete. Tell the user: "Superhero skill is ready! You can now post, read, trade tokens, and check trending content."
