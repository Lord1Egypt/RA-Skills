---
name: saturnzap
description: "Non-custodial Lightning wallet for AI agents via `sz` CLI: send/receive sats, pay invoices, auto-pay HTTP 402 (L402), manage channels and liquidity. Use when: (1) paying for API access with Lightning, (2) creating or paying BOLT11 invoices, (3) checking wallet balance or channel health, (4) managing peers and channels. NOT for: on-chain-only Bitcoin transactions, custodial Lightning services."
homepage: https://github.com/lqwdtech/SaturnZap
metadata:
  { "openclaw": { "emoji": "⚡", "os": ["linux"], "requires": { "bins": ["sz"], "env": ["SZ_PASSPHRASE"] }, "optionalEnv": ["SZ_MCP_MAX_SPEND_SATS", "SZ_CLI_MAX_SPEND_SATS", "SZ_NETWORK", "SZ_REGION", "SZ_MAINNET_CONFIRM", "SZ_PRETTY", "SZ_ALIAS", "SZ_TRUSTED_PEERS_NO_RESERVE", "SZ_ESPLORA_URL"], "primaryEnv": "SZ_PASSPHRASE", "install": [{ "id": "uv", "kind": "uv", "package": "saturnzap", "bins": ["sz"], "label": "Install SaturnZap (uv)" }] } }
---

# SaturnZap Lightning Wallet

Non-custodial Lightning Network wallet for autonomous AI agents. All output is JSON by default — no `--json` flag needed. Parse stdout for success (`"status": "ok"`) and stderr for errors (`"status": "error"`).

See `{baseDir}/references/json-contracts.md` for full JSON output shapes.
For deep agent integration scenarios, error recovery trees, and anti-patterns, see `docs/agent-guide.md`.

## Quick Decision — 5 Most Common Agent Actions

```bash
# 1. First-time setup (idempotent, one command)
sz setup --auto

# 2. Pay for API access (L402, with spending cap)
sz fetch "https://api.example.com/data" --max-sats 100

# 3. Check if operational
sz status  # parse: synced, peer_count > 0, usable_channel_count > 0

# 4. Receive payment (blocking)
sz invoice --amount-sats 1000 --memo "service fee" --wait

# 5. Send a Lightning payment (with cap)
sz pay --invoice "lnbc..." --max-sats 5000
```

## When to Use

✅ **USE this skill when:**

- Paying for API access via Lightning (L402 / HTTP 402 auto-pay)
- Creating BOLT11 invoices to receive payments
- Paying BOLT11 invoices or sending keysend payments
- Checking wallet balance (on-chain + Lightning)
- Opening, closing, or listing Lightning channels
- Connecting to or managing Lightning peers
- Monitoring channel liquidity health
- Requesting inbound liquidity from an LSP

## When NOT to Use

❌ **DON'T use this skill when:**

- On-chain-only Bitcoin transactions (use a Bitcoin wallet CLI)
- Custodial Lightning services (use hosted APIs like Strike, LNBits)
- Non-Lightning crypto payments (ETH, stablecoins, etc.)
- Mainnet is the default network. Use `--network signet` for development and testing with free test coins.

## Setup

```bash
# Install (one-time) — one-line installer handles uv + the vendored ldk-node wheel
curl -LsSf https://raw.githubusercontent.com/lqwdtech/SaturnZap/main/install.sh | sh

# Or, if you prefer the explicit uv invocation:
# uv tool install saturnzap \
#   --find-links https://github.com/lqwdtech/SaturnZap/releases/expanded_assets/v1.3.1

# Set passphrase (required — encrypts the seed on disk)
export SZ_PASSPHRASE="your-secure-passphrase"

# Initialize wallet (first time only — generates BIP39 seed, starts node)
# RECOMMENDED for agent hosts: write the mnemonic to a mode-0600 file instead
# of stdout, so it never lands in tool-call transcripts or orchestrator logs.
sz init --backup-to ~/.saturnzap-mnemonic --no-mnemonic-stdout

# Or, for the LQWDClaw faucet on mainnet (sets a readable alias):
sz init --for-lqwd-faucet --backup-to ~/.saturnzap-mnemonic --no-mnemonic-stdout

# Interactive operators can omit the flags; the mnemonic prints once for backup:
# sz init

# Verify node is running
sz status

# Recommended: keep the node alive across reboots (systemd)
sz service install
```

### Passphrase injection — pick the safest available option

In order of preference:

1. **Systemd `EnvironmentFile=` (recommended for production agents).**
   `sz service install` writes `/etc/saturnzap/saturnzap.env` (mode 0600,
   owner-only) and references it from the systemd unit. The unit file itself
   contains no secrets.
2. **Secret store / environment injection** at the agent runtime layer
   (Vault, 1Password CLI, doppler, AWS Secrets Manager, etc.) writing
   `SZ_PASSPHRASE` into the process environment.
3. **Shell `export`** in a non-shared session — fine for local development.
4. **`openclaw.json` (development/testing only).** This stores the passphrase
   at rest in a config file. Use only on isolated dev machines and only when
   the file is mode-0600 in an encrypted home directory:

   ```json
   {
     "skills": {
       "entries": {
         "saturnzap": {
           "enabled": true,
           "env": { "SZ_PASSPHRASE": "your-dev-passphrase" }
         }
       }
     }
   }
   ```
   Do not use this path for wallets holding production funds.

## Security Model — Why This Skill Is Flagged "Suspicious" (And Why That's Correct)

SaturnZap is a **self-custodial Lightning wallet**. The ClawHub security scanner
correctly flags four behaviors that are inherent to any self-custodial wallet. If
you're evaluating this skill, read this section before installing.

**1. Installs a vendored wheel from GitHub Releases.** The `--find-links` flag pulls
the `ldk-node` Python bindings wheel from the SaturnZap GitHub Releases page. This is
because `ldk-node` is not yet published to PyPI. The wheel is built from the official
LDK Node v0.7.0 source, vendored in-repo at `vendor/ldk_node-0.7.0-py3-none-any.whl`,
and its SHA256 is pinned in `vendor/ldk_node.sha256` (verified in CI on every push).

**2. Emits a BIP39 mnemonic on first init.** `sz init` prints the 24-word recovery
phrase **exactly once**, to stdout, so the operator can back it up. It is never
re-emitted by any other command. It is also never sent over the network. Losing the
mnemonic means losing the funds; that is the self-custody tradeoff.

**3. Passphrase injection via `openclaw.json`.** The passphrase decrypts the seed
file (Fernet AES-128 + PBKDF2, 600k iterations). It must be available on every
wallet operation. Two options:
- **Environment variable (recommended):** `export SZ_PASSPHRASE=...` in your shell
  profile or systemd unit. Never written to disk by SaturnZap.
- **`openclaw.json`:** convenient for agents, but the passphrase lives in that file
  at rest. Use only if the file itself is protected (`0600`, encrypted home dir,
  etc.).

**4. Optional systemd service.** `sz service install` is **optional**. It keeps the
Lightning node running across reboots, which is necessary for payments to clear
reliably. The service runs as the invoking user, writes state under
`~/.local/share/saturnzap/<network>/`, and does not escalate privileges beyond
opening port 9735 via UFW if UFW is active.

**What this skill does NOT do:**
- Transmit the seed or passphrase anywhere
- Contact any server except Esplora (Bitcoin chain data) and peers you explicitly add
- Run with elevated privileges
- Modify any system config outside the Lightning listen port

**Operator responsibilities:**
- Back up the 24-word mnemonic offline before funding the wallet
- Use a strong passphrase (12+ chars; minimum enforced at init)
- Set `SZ_MCP_MAX_SPEND_SATS` to cap agent spending
- Review `docs/security-scenarios.md` in the SaturnZap repo for the full threat model

For the full security architecture, see
[docs/security-scenarios.md](https://github.com/lqwdtech/SaturnZap/blob/main/docs/security-scenarios.md).

## Node Management

```bash
# Guided first-run (idempotent — skips completed steps)
sz setup

# Non-interactive setup: init + address + request inbound from LQWD
sz setup --auto

# Initialize wallet (first time — writes seed, starts node)
sz init

# Start node (auto-starts from encrypted seed)
# NOTE: 'sz start' runs as a foreground daemon and blocks until SIGTERM/SIGINT.
# For agents/scripts, prefer 'sz service install' (systemd) or let commands
# auto-start the node on demand. Use 'sz start --foreground' for the legacy
# "print status and exit" behaviour.
sz start

# Stop node
sz stop

# Stop node and cooperatively close all channels first
sz stop --close-all

# Check node status (pubkey, sync state, peer/channel counts)
sz status

# Get connection URI to share with other wallets (pubkey@host:port)
sz connect-info
```

The node auto-starts when needed. Most commands call `sz start` internally if the node isn't running.

**For agents:** Prefer `sz setup --auto` over `sz init` — it's idempotent and handles the full first-run flow in one command.

## Wallet

```bash
# Get a new on-chain address (for receiving signet faucet deposits)
sz address

# Send sats on-chain to an address
sz send <address> --amount 50000

# Send ALL on-chain sats to an address
sz send <address>

# Check balances (on-chain + lightning + per-channel breakdown)
sz balance
```

Payment commands (`pay`, `keysend`, `send`) include pre-flight balance checks — they return a clear `INSUFFICIENT_FUNDS` error with the current balance if funds are too low.

## Payments

```bash
# Create invoice to receive 1000 sats
sz invoice --amount-sats 1000 --memo "payment for data"

# Create invoice and wait until paid (blocks until payment or expiry)
sz invoice --amount-sats 1000 --memo "service fee" --wait

# Create variable-amount invoice (payer chooses amount)
sz invoice --amount-sats 0 --memo "tips welcome"

# Pay a BOLT11 invoice (with optional spending cap)
sz pay --invoice "lnbc..." --max-sats 5000

# Send spontaneous keysend payment
sz keysend --pubkey "03abc..." --amount-sats 500

# View payment history
sz transactions --limit 10
```

### Spending Caps

Always use `--max-sats` when paying invoices on behalf of a user to enforce a spending limit. If the invoice exceeds the cap, the payment is rejected with a `SPENDING_CAP_EXCEEDED` error.

## L402 (HTTP 402 Auto-Pay)

Fetch a URL and automatically pay the Lightning invoice if the server returns HTTP 402:

```bash
# Basic L402 fetch
sz fetch "https://api.example.com/premium-data"

# With spending cap (recommended for agent use)
sz fetch "https://api.example.com/data" --max-sats 100

# POST with headers and body
sz fetch "https://api.example.com/submit" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "analysis"}' \
  --max-sats 500

# Custom timeout
sz fetch "https://api.example.com/slow" --timeout 60
```

The response includes the HTTP status, body (parsed as JSON if possible), and payment details if a 402 was paid.

## Channels

```bash
# List all channels
sz channels list

# Open a channel to a specific peer
sz channels open --peer "03abc...@1.2.3.4:9735" --amount-sats 100000

# Open a channel via LQWD LSP (defaults to LQWD-AI-Grid on mainnet — LSPS1/LSPS2 JIT-capable)
sz channels open --lsp lqwd --amount-sats 100000

# Open a channel via a specific LQWD region (e.g. Japan)
sz channels open --lsp lqwd --region JP --amount-sats 200000

# Close a channel cooperatively
sz channels close --channel-id "abc123" --counterparty "03abc..."

# Force-close a channel
sz channels close --channel-id "abc123" --counterparty "03abc..." --force

# Wait for a channel to become usable (blocks until ready or timeout)
sz channels wait --channel-id "abc123" --timeout 300
```

**Minimum channel sizes:** LQWD nodes require at least 2,000,000 sats per channel. If the peer rejects, `sz` returns a `CHANNEL_REJECTED` error with the reason (e.g. "below min chan size").

## Peers

```bash
# List connected peers
sz peers list

# Connect to a peer
sz peers add "03abc...@1.2.3.4:9735"

# Disconnect a peer
sz peers remove "03abc..."

# Trusted peers (waive anchor reserve + allow 0-conf channels).
# The full LQWD fleet is trusted by default on mainnet.
sz peers trusted-list
sz peers trust "03abc..."
sz peers untrust "03abc..."
```

## Config

```bash
# Inspect and edit ~/.config/saturnzap/config.toml programmatically.
sz config list
sz config get node.alias
sz config set node.alias "my-agent"
sz config set node.listen_port 9735
sz config unset esplora_url
```

Changes apply on the next node start. Known keys: `node.alias`,
`node.listen_port`, `node.min_confirms`, `node.trusted_peers_no_reserve`,
`esplora_url`, `network`.

## Liquidity

```bash
# Channel health report (scores, labels, recommendations)
sz liquidity status

# Request inbound liquidity from LQWD (auto-selects nearest region)
sz liquidity request-inbound --amount-sats 100000

# Request inbound from a specific region
sz liquidity request-inbound --amount-sats 100000 --region CA
```

Health scores range 0–100. Labels: `healthy` (40+), `warning` (20–40), `critical` (0–20).

Channels with offline peers are flagged as stale with force-close recommendations.

## Service Management

```bash
# Install and start SaturnZap as a systemd service (persistent node)
sz service install

# Check service status
sz service status

# Remove the systemd service
sz service uninstall
```

When the systemd service is running, the node stays up between CLI calls (no per-command startup overhead).

## Guardrails

- **Always use `--max-sats`** on `sz pay` and `sz fetch` to enforce spending caps. Never pay unbounded invoices autonomously.
- **Never expose the mnemonic** — the seed phrase from `sz init` must never appear in chat, logs, or tool output after initial display.
- **Check balance first** — payment commands now check balance automatically and return `INSUFFICIENT_FUNDS` with the current balance. You can also run `sz balance` before large payments.
- **Parse JSON output** — all `sz` commands output JSON to stdout on success, stderr on error. Use the `status` field to branch logic.
- **Check for warnings** — `sz pay`, `sz keysend`, `sz balance`, and `sz fetch` may include a `"warnings"` array when channel capacity is low or no channels exist. Act on warnings: open a channel, request inbound liquidity, or log for review.
- **Verify connectivity** — after setup, run `sz connect-info --check` to confirm the Lightning port is reachable. If `"reachable"` is `false`, the firewall may be blocking peers.
- **Mainnet by default** — SaturnZap defaults to Bitcoin mainnet (real sats). Use `--network signet` for testing. Always use `--max-sats` spending caps on mainnet.
- **Passphrase security** — `SZ_PASSPHRASE` encrypts the seed on disk. Keep it out of chat and logs.

## Workflow Templates

### Pay for API Access (L402)

```bash
# Check balance first
sz balance

# Fetch a paid endpoint with a spending cap
sz fetch "https://api.example.com/premium" --max-sats 100
```

### Receive a Payment

```bash
# Create an invoice and wait until paid (recommended for agents)
sz invoice --amount-sats 1000 --memo "service fee" --wait

# Or: create invoice, share it, then poll manually
sz invoice --amount-sats 1000 --memo "service fee"
# Share the `invoice` field from the JSON output with the payer
sz transactions --limit 1
```

### Check Channel Health

```bash
# Overall health report with recommendations
sz liquidity status

# Detailed balance breakdown
sz balance
```

### Open a Channel and Send Payment

```bash
# Open a channel
sz channels open --lsp lqwd --amount-sats 100000

# Wait for channel to become usable
sz channels wait --timeout 300

# Pay an invoice once the channel is ready
sz pay --invoice "lnbc..." --max-sats 5000
```

## Notes

- All output is JSON. Use `--pretty` or `SZ_PRETTY=1` for human-readable formatting.
- The node auto-starts from the encrypted seed when any command needs it. Explicit `sz start` is rarely needed.
- LQWD region codes: `AI` (LQWD-AI-Grid, default on mainnet, LSPS1/LSPS2 JIT-capable), `NEAREST` (timezone-based fallback), or a specific country: CA, US, SE, FR, GB, IE, IT, DE, BH, JP, AU, SG, HK, KR, ID, IN, BR, ZA.
- `sz fetch` caches L402 tokens — repeated requests to the same endpoint reuse the token without re-paying.
