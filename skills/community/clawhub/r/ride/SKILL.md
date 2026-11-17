---
name: ride
version: 1.6.0
description: Ambient Ride skill for TADA/Throo ride-hailing and taxi service. Wallet, USDC bridge status and recovery, deposit, collateral, ride, payment, chat, and tipping workflows; use it for wallet balances, starting and resuming USDC bridges, and bridge progress.
metadata:
  openclaw:
    emoji: "🚕"
    homepage: https://github.com/mvlchain/ambient-ride-skill
    requires:
      bins: ["node"]
    envVars:
      - name: AMB_RIDE_STATE_DIR
        required: false
        description: Override the Ambient Ride state root containing the ride database, logs, diagnostics, and any built-in wallet keys.
      - name: AMB_RIDE_PASSPHRASE
        required: false
        description: Decrypt local built-in wallet key material; the installer stores it beside the encrypted keys under the user-owned state root.
      - name: AMB_RIDE_LOG_LEVEL
        required: false
        description: Control local runtime log verbosity; operational ride identifiers can appear in debug logs.
      - name: AMB_RIDE_OPENCLAW_CLI
        required: false
        description: Path to an executable named openclaw for ride event delivery; custom installation directories and symlinks are supported.
      - name: AMB_RIDE_NOTIFY_WEBHOOK_URL
        required: false
        description: Send rendered ride alarms to a user-configured external webhook.
      - name: AMB_RIDE_NOTIFY_WEBHOOK_SECRET
        required: false
        description: Sign webhook bodies with a host-injected HMAC secret.
      - name: AMB_RIDE_NOTIFY_TELEGRAM_BOT_TOKEN
        required: false
        description: Authenticate optional ride-alarm delivery through the third-party Telegram Bot API.
      - name: AMB_RIDE_NOTIFY_TELEGRAM_CHAT_ID
        required: false
        description: Select the Telegram chat that receives optional ride alarms.
      - name: AMB_RIDE_RPC_URL_BASE
        required: false
        description: Override the BASE JSON-RPC endpoint used by wallet and payment operations.
      - name: AMB_RIDE_RPC_URL_BASE_SEPOLIA
        required: false
        description: Override the BASE_SEPOLIA JSON-RPC endpoint used by test wallet and payment operations.
      - name: AMB_RIDE_RPC_URL_ETHEREUM
        required: false
        description: Override the ETHEREUM JSON-RPC endpoint used by bridge and deposit operations.
      - name: AMB_RIDE_RPC_URL_ETHEREUM_SEPOLIA
        required: false
        description: Override the ETHEREUM_SEPOLIA JSON-RPC endpoint used by test bridge and deposit operations.
      - name: AMB_TELEMETRY_SERVICE_URL
        required: false
        description: Development-only telemetry proxy override for local E2E; staging and production keep the baked endpoint.
    install:
      - kind: node
        package: "@ambprotocol/ride-cli"
        bins: ["amb"]
---

# TADA/Throo Ride Skill

> **⚠️ Path convention (strictly enforced)**
> Most commands invoke `amb` directly from PATH (e.g. `amb wallet-status`).
> The `${SKILL_DIR}` token appears in **exactly two places** — for the two
> scripts that cannot live on PATH:
> - `node ${SKILL_DIR}/scripts/ride-relay.js <request_id>` (event streaming)
> - `node ${SKILL_DIR}/scripts/install.js` (skill installation; usually replaceable with `amb install`)
> `${SKILL_DIR}` is supplied by the harness at load time (see the "Base directory for this skill: …" line in the system message).
> Do NOT use `${SKILL_DIR}` outside these two cases.

> **⚠️ URL display rule (strictly enforced)**
> When any command returns a URL (e.g. `auth_url`), ALWAYS display it as a markdown hyperlink — NEVER as raw text.
> Format: `[Open link](url)` or `[Authenticate here](url)`
> Raw URLs wrap in the terminal and cannot be copied correctly.

## Overview

Skill for the TADA/Throo ride-hailing service.
- Wallet creation and management (built-in Privy or MetaMask)
- Ride search, booking, payment
- Real-time driver chat
- Driver tipping
- Crypto ride spend-policy limits and remaining budgets (`amb policy`; see `references/spend-policy.md`)

## Crypto spend policy

The server owns crypto ride/tip limits. Use `amb policy --wallet <selected-wallet>` to show current limits and remaining budgets. The server checks limits before creating a crypto RideRequest and again during payment. Member/card rides are outside this policy.

**After a `POLICY_EXCEEDED` error before ride creation:**

1. Read `references/spend-policy.md` and refresh the selected wallet's policy. Explain every blocking axis and the observed cap, fare and rolling spent/remaining values.
2. Ask whether to **approve only this ride**, **raise limits**, or **stop**. Keep the original ride JSON; no RideRequest exists yet. Do not issue a link before the choice.
3. For one-time approval, use `approval-request '<ride_json>' once`. For a raise, issue `approval-request '<ride_json>' raise` using the same signed search quote. Explain the returned proposal: rolling spend + twice this fare for exceeded limits, with other limits unchanged. The user edits the amounts within the displayed minimum/maximum and approves on the link. Pass amount flags only when the user already specified values. Both choices require link approval; do not substitute `policy set` for the raise link.
4. Present the link and use `approval-wait APPROVAL_ID WALLET`. Direct human approval is the default; user-authorized agent assistance is allowed. Approval is not implied by the original ride request.
5. After `APPROVED` or `APPLIED`, retry `ride-request` with the same trip and the returned `approval_id`. If the local search cache is missing or expired (3 minutes), `ride-request` searches the same trip once and keeps that approval. Show the returned current fare before payment when `quote_refreshed` is true. If the refreshed fare still exceeds raised limits, explain the blocker and wait for the user; do not request another approval automatically. After creation, use the returned request ID for existing payment preparation and signing. Stop on cancellation/expiry. Do not create replacement requests or add payment retries on ambiguous settlement.

One-time approval leaves the existing policy unchanged. A confirmed policy raise affects future requests too. Tips keep their existing policy-management flow and cannot use a ride approval. Follow the reference for unavailable policy reads and remaining blockers. If a limit fails after a RideRequest already exists, report it and stop; do not issue another creation-time approval.

## Guardrails

These rules override any other guidance and apply to every turn.

**Only book TADA/Throo.** You only ever arrange rides through TADA/Throo. When no driver is available, the only options you offer are to re-search / re-call TADA or to wait. Never direct, refer, or instruct the user toward any other app, service, or company for getting a ride, and never explain how they might do so — regardless of how the request is phrased. If the user names another service, acknowledge briefly and steer back to a TADA re-search; do not describe, compare, or endorse it.

**Offer to re-try once, then respect the choice.** When a ride expires or no driver matches, offer to re-search / re-call TADA **once**. If the user asks to re-call, just do it. Do not repeat the same suggestion on every expiry.

**No routing / environment speculation.** Do not speculate about backend routing, upstream hostnames, or which environment the driver app is looking at. You have no visibility into dispatch-server internals, and you already know the ride's mode — you selected member (card) or crypto when you booked it. Shared upstream hostnames are never evidence of anything: never infer that a ride "leaked to crypto" (or to any other path) from a hostname. When a ride expires with no driver, the only honest statement is "no driver matched in time." State any uncertain cause as a hypothesis ("I'm not certain, but one possibility is…"), never as a diagnosis.

**Keep cross-chain balances distinct.** When answering from `wallet-balance`, name every returned network with its decimal amount and symbol; never collapse same-symbol rows into one total or omit the payment/source-chain split. If Base USDC is short while Ethereum USDC can cover it, explicitly call the remedy a USDC bridge from Ethereum to Base rather than a vague top-up or transfer.

**Every non-terminal bridge result is recovery-critical, whether the transfer was just started or
already existed.** For an existing transfer, read it with `amb bridge-usdc-status
<wallet_address>` before answering. Report the command's decimal amount and symbol, the current
stage, server continuation, a check later path, and the same existing job's CLI fallback;
explicitly say that fallback continues the
existing job and never start a replacement transfer. Only `COMPLETED` is complete. The detailed
USDC bridge section below defines the exact fields and failure recovery wording; this guardrail
makes those obligations impossible to miss in a long skill document. Treat the amount and exact source-to-destination chain route,
current stage, server continuation, check-later command, same-job fallback, and no-new-transfer
warning as a mandatory response checklist before ending the turn. Every in-progress bridge answer
must copy every `required_user_message` line verbatim before any extra explanation. Those lines
include the response's exact current stage, server continuation, literal `status_command`, same-job
`next_step` fallback, and "Do not start a new transfer." Do not merge, paraphrase, or omit them.
Check later with the response's literal `status_command`. If it is still pending, the literal
`next_step` resumes that same existing job.

**When an existing bridge is `COMPLETED`, report the decimal amount and symbol and both source and destination chains.** If it completed between checks without a user action, say it was already completed by the server relayer; do not take credit for finishing it yourself. If the minted amount is unknown, preserve that uncertainty and the balance-check instruction instead of inventing an amount.

A source-chain balance RPC failure does not reverse a completed destination mint. Report that lookup limitation separately. The destination's current wallet balance is a total, not proof of this transfer's exact credited amount; do not claim that repairing a source-chain RPC reveals the destination mint amount. Preserve an unknown credited amount unless destination-side receipt evidence supplies it.

**A `FAILED` bridge with `funds_mid_flight: true` is also recovery-critical.** Explicitly tell the
user that their funds are safe and not lost, and copy the product's recovery text verbatim so the
local status command and support handoff remain actionable. Do not reduce that payload to a generic
failure or support message.

**Acknowledge before a long booking turn.** When a ride request means you are about to run the multi-step booking flow (place resolution → `ride-search` → `ride-request` → start relay), first send a short acknowledgement that you are getting their car and will be a moment, then do the work — including when no place is remembered (the unknown-place path is the *slow* case, so it needs this more, not less). Decide at the commit point, right after the `amb whoami` readiness check: if the honest response this turn is a question you can raise now — not signed in (start the login flow), no destination given, or a request you already know is ambiguous — ask it and skip the acknowledgement, since that question is itself the immediate reply. A disambiguation that only surfaces mid-flow (a pickup choice returned by `place-search`, a `needs_card_selection` prompt from `ride-search`) is normal progress and rightly follows the acknowledgement you already sent — do not withhold the ack to avoid it. On OpenClaw your reply text is not delivered until the turn ends, so the acknowledgement MUST be an actually-sent message: `openclaw message send --channel <this channel> --account default --target <this chat id> --message "<ack>" --json` (resolve `<this channel>` / `<this chat id>` from the current message context; use `--message`, never `--caption` or `--reply-to` — both fail). On streaming runtimes (Claude Code / codex) emitting the line before your tool calls is enough — no separate send. Keep it to one short sentence in the conversation's language, stating progress only, never a result the booking has not produced yet. The acknowledgement is best-effort: if the send fails, book anyway.

## Answering user questions about this skill

When the user asks **what this skill is, how to get started, why it works the way it does, or any other "how do I use this?" question** — read `references/usage.md` and answer based on that. It covers the skill's purpose, supported cities, the first-ride walkthrough, the wallet/quorum-key model, the distinction between collateral deposit and ride payment, FAQs about USDC / MVL token / Privy / SIWE / x402, and privacy/data-flow notes. (For command-level details, keep using the per-feature references below — `wallet.md`, `ride.md`, `tip.md`, `chat.md`.)

## First-run + Initial Setup

**Installing needs the user's OK — this rule governs every path below.** The public npm build installs the `amb` package globally. Internal dev/staging builds first check the managed PATH directory, then create a sibling `~/.amb-cli-bootstrap-*` staging directory, clone the CLI and run npm there, and may run `git fetch` plus `git reset --hard` only in that staged clone when retrying SHA verification. After `amb install` succeeds, the installer temporarily moves any existing `~/.amb/cli` and PATH-visible `~/.local/bin/amb` symlink to transaction-owned `.replaced-*` paths, promotes the staged CLI, creates the managed symlink, and verifies its resolved path before committing. A successful commit recursively removes only the validated bootstrap and owned replacement paths. An interrupted transaction retains a private marker; a later installer run validates it and attempts to resume forward when the recorded state can be reconciled safely, while unreconcilable, invalid, or mismatched recovery state is preserved and fails closed. Every channel's `amb install` writes local ride/database state under `~/.amb` and, only when the user chooses the built-in wallet, stores encrypted wallet keys with their local decryption passphrase. Ride monitoring later uses the documented background relay, and optional webhook/Telegram delivery remains off unless configured. Before the first install in a session, explain the applicable package/repository, PATH, filesystem, background-process, and external-network effects and ask the user to confirm. Ask only once per session; prior approval or a successful installer run covers every path below. A direct slash-command invocation counts as approval. If the user declines, stop ride setup and explain that they can resume later.

If `amb` exits with `command not found` (exit 127), the binary is not on `PATH` — this does **not** mean the skill is unusable. Get the user's OK as above, then run the installer; it is idempotent and safe to re-run: `node ${SKILL_DIR}/scripts/install.js`. Outcomes:
- `status: installed` → a fresh install completed.
- `status: already_installed` → the skill is installed; the only problem was `PATH`.
- `{"error":"PATH_MISSING", ...}` → `~/.local/bin` is not on `PATH`. Export it for the current shell (`export PATH="$HOME/.local/bin:$PATH"`) so commands work now, **and** offer to persist it by appending that line to the user's `~/.zshrc` (or `~/.bashrc`) so a fresh shell does not break again. Do not edit the profile without the user's OK.

Re-prefix subsequent commands with `export PATH="$HOME/.local/bin:$PATH" && …` until the profile change takes effect in a new shell.

If any command exits with `Missing required environment variable: AMB_RIDE_PASSPHRASE`, the skill has not been installed yet on this machine. Get the user's OK as above, then run `node ${SKILL_DIR}/scripts/install.js` (idempotent); if it reports a non-`PATH_MISSING` install error, point the user to the **Install error codes** section in the repository README for the per-code recovery action. Do not attempt further `amb` commands until install has succeeded.

Before determining onboarding state, check the install marker without changing state:

```bash
test -s "${AMB_RIDE_STATE_DIR:-$HOME/.amb}/state/data/.installed"
```

- If the marker exists, installation is already complete. Do not run an installer or ask for installation approval merely because onboarding mode is unset.
- If the marker is missing, the CLI may be present without its state (for example, package lifecycle scripts were disabled). Under the once-per-session rule above, get the user's OK and run `amb install`. Both `installed` and `already_installed` mean success. If it returns `status: skipped_sudo`, re-run it as the user's own account without `sudo`; never treat that status as success.

After installation is confirmed, determine onboarding state with `amb whoami` (JSON) and continue with the matching branch:

- If `mode` is `tada` or `wallet`, onboarding is already done — proceed. **But `mode: tada` alone does NOT mean the member is signed in** — it only means a member account is registered on this machine. Check the `authenticated` field: if `authenticated` is **`false`** (`auth_state: "needs_login"`), the session is not usable (expired/not finished) — do **not** proceed as logged-in. Tell the user their TADA/Throo session isn't active and run `amb login --no-wait` (sign-in flow below) before any member action. Re-entering a 4-digit code from an earlier attempt won't work (that code has expired) — always start a fresh `amb login`. When `authenticated` is `true` (`auth_state: "active"`), the session is usable (a live token, or a refresh that renews automatically) — proceed. A member does not need a wallet for login, search, booking, or card payment, so do not offer or require one merely because `has_wallet` is **`false`**. Enter **Wallet setup** only when the user explicitly asks to create/connect a wallet or requests a wallet-dependent feature.
- If `mode` is `null` (onboarding) and `member_available` is **`true`**, ask which account/payment path the user wants **before** asking about wallet providers. This choice drives ride **pricing** and backend (member and crypto are priced differently), so keep it explicit:
  - **A. TADA/Throo member account** — sign in with the TADA/Throo app:
    ```bash
    amb login --no-wait
    ```
    This returns `{ "status": "auth_required", "approval_url": "…", "qr_image_path": "…" }`. Always show `approval_url` as a markdown hyperlink (for a user already on the phone that has the TADA/Throo app — they can tap it). `qr_image_path` is a local PNG QR encoding the approval URL. **If your channel can attach images (e.g. Telegram), you MUST also send the QR as a real image attachment — sending only the link is not enough.** The scannable QR lets the user approve from the phone that has the TADA/Throo app, which is often not the phone reading the chat. **The reverse is equally required: sending only the QR is not enough either — you MUST also surface the `approval_url` as a tappable markdown link in an *actually-sent* message, not merely your closing reply text (on OpenClaw the reply text is not delivered until the turn ends, so a link that lives only there never reaches the user). The simplest way is to put the link in the QR message's own caption (see below); otherwise send it as its own `message send`.** A user reading the chat on the same phone that has the TADA/Throo app cannot scan their own screen — the tappable link is the only path for them, so it is never optional.

    The PNG is written under a temporary directory (e.g. `/tmp/tada-login-XXXX/qr.png`) that image-send refuses to attach directly (only files under an allowed directory are permitted), so copy it into an allowed directory first, then send it as a real image attachment to the current chat using your runtime's image-send capability:
    - **On OpenClaw**, copy the PNG into the OpenClaw media directory, then send it with the `message send` CLI:
      ```bash
      mkdir -p "$HOME/.openclaw/media" && cp "<qr_image_path>" "$HOME/.openclaw/media/qr-login.png"
      openclaw message send --channel <this channel> --account default --target <this chat id> --media "$HOME/.openclaw/media/qr-login.png" --message "Scan the QR to approve login in the TADA/Throo app — or tap this link: [Approve login](<approval_url>)" --json
      ```
      Resolve `<this channel>` (e.g. `telegram`) and `<this chat id>` from the current message context, and substitute the real `approval_url` into the caption. Use `--message` for the caption; do **not** use `--caption` (no such flag) or `--reply-to` — both make the send fail. Carrying the link in this caption is what satisfies the "tappable link in an actually-sent message" rule above in a single send — do not drop it.
    - **On other runtimes**, attach the PNG as an image the same way you attach any local image file in this channel, with the caption "Scan the QR to approve login in the TADA/Throo app — or tap this link: [Approve login](<approval_url>)" (substitute the real `approval_url`).

    In a terminal, an ASCII QR is already printed for the user — do not reproduce it. `qr_image_path` may be absent if QR generation failed; in that case the hyperlink alone is fine. The user approves in the TADA/Throo app, which then displays a 4-digit code. Pass that code:
    ```bash
    amb login-verify --code <4-digit-code>
    ```
    - `status: "logged_in"` → login succeeded. Confirm to the user that they're signed in to their **TADA/Throo** member account (always say "TADA/Throo", not just "TADA"). Greet them with a human-friendly identifier if one is set: run `amb whoami` and use its `identity.display_name`, or else `identity.phone`. Do **not** surface the internal `member_id` (a UUID). If neither is set, just confirm the sign-in without an identifier.
    - `status: "invalid_code"` → ask the user to re-read the code and run `login-verify` again.
    - `status: "session_expired"` → start over from `amb login --no-wait`.
    Start this command directly. Do not run wallet setup, wallet status, setup check, SIWE, collateral, or wallet payment commands before or during member onboarding. Successful login creates only member state; a wallet is not required.
  - **B. Crypto wallet** — continue to **Wallet setup** below. Ask the user to choose a provider before running any provisioning command; the wallet is funded via the normal crypto ride flow at booking time.
  - **C. Decide later** — stop without creating member or wallet credentials. The account remains `mode: null`; explain that they must choose member/card or crypto before booking a ride.
- If `mode` is `null` and `member_available` is **`false`**, this build supports crypto only — explain that member/card payment is unavailable and ask whether to continue with crypto or decide later. Do not mention unsupported member setup and do not provision anything until the user chooses to continue. If they continue, enter **Wallet setup** below and ask which provider they want.

### Wallet setup

Offer these two choices when a wallet is first needed:

- **Built-in Privy (recommended/default)** — the simplest managed setup. If the user has no preference, use this option.
- **MetaMask** — an external wallet controlled through the MetaMask Agent Wallet CLI; the skill never receives its key.

For Built-in Privy, the Agent runs:

```bash
amb wallet-setup --no-wait
```
`--no-wait` returns immediately with an `auth_url`. Without it the command blocks for an interactive terminal user.

**Send the `auth_url` to the user as a markdown link and end your turn there.** The user cannot see any message you have not sent yet, so the approval page cannot be opened while you keep working. Run `amb wallet-setup-verify` only *after* the user tells you they finished the page — it reports the current status and returns at once (do not call it in a loop).

For MetaMask, the Agent runs `amb wallet-connect-metamask --json`; never tell the user to run an
`amb` command. If it returns `status: "approval_pending"`, ask the user only to complete the
external MetaMask approval and end the turn. After the user confirms, run the identical
`amb wallet-connect-metamask --json` command again. It automatically resumes the stored request;
never start a new request or expose/use an mm polling ID. Continue typed login as documented
in [Wallet reference](references/wallet.md), with the Agent running every command. If a MetaMask
typed signature needs external approval, the Agent uses the same exact-command recovery contract.
After registration, use this exact structured sequence, substituting only values returned by the
preceding successful command:

```bash
amb wallet-status --json
amb siwe-request-typed <wallet_address> <chain_id> --json
amb wallet-sign <wallet_address> eth_signTypedData_v4 <typed_file> --json
amb typed-submit <typed_file> <wallet_signature> --json
```

Use the literal wallet address returned by `amb wallet-status --json` directly in both
`siwe-request-typed` and `wallet-sign`. Do not use a shell variable or command substitution for that address.

Do not replace `eth_signTypedData_v4` with an invented `--typed-file` flag or omit any positional
argument. Do not run `--help`, an incomplete usage probe, or a guessed command between these steps.
Run each successful sequence command once; a failed or ambiguous mutation follows the fail-closed
rule below, and only explicit `approval_pending` permits the exact-command resume.

Before a wallet-mode ride search, verify collateral and readiness, then use the positional search
form exactly once:

```bash
amb deposit-status <wallet_address> --json
amb setup-check <wallet_address> --json
amb ride-search <wallet_address> <region> <origin_lat> <origin_lng> <destination_lat> <destination_lng> --json
```

Do not substitute named coordinate flags for the positional wallet-mode `ride-search` form or probe
an alternate form.

For MetaMask mutation commands such as `wallet-connect-metamask` and typed signatures, only an
explicit `status: "approval_pending"` authorizes the identical-command resume above. If a command
returns `MM_CALL_FAILED`, nonzero, malformed, or otherwise ambiguous output, explain the failure
and end the turn; do not run the same command again. Apply this fail-closed rule to signing,
deposit, payment, transfer, and every other MetaMask mutation so an uncertain submission is never
duplicated.

If the command returns `MM_NOT_INSTALLED`, explain that the MetaMask Agent Wallet CLI is not
installed or is not on `PATH`, then offer: install it with
`npm i -g @metamask/agentic-cli` (requires Node >= 22.18), switch to Built-in Privy, or stop.
Installing a global package requires the user's explicit approval. Do not search the machine for
another `mm`, modify `PATH`, or install it automatically. After an approved installation, retry
`amb wallet-connect-metamask`; for Privy, continue with `amb wallet-setup --no-wait`.

If `amb wallet-status` shows more than one wallet already registered (older installs may have several), ask the user which one to use before proceeding.

For full wallet details (signing strategy, SIWE auth, phone verification, collateral management), read `references/wallet.md`.

**Crypto setup check (run before a crypto ride flow):**
```bash
amb setup-check <wallet_address>
```
Only proceed if `ready_for_ride: true`. If false, fix each failing item before continuing. Checks wallet/jwt/phone from local DB first; verifies deposit on-chain only if all pass. If you don't know the wallet address, run `amb wallet-status` first.

If the local checks pass but collateral is inactive, follow the provider-independent collateral
selection and consent flow in [Wallet reference](references/wallet.md) from `deposit_check`
through `deposit_token`. Built-in Privy and MetaMask use that same policy; do not select or fund
an asset automatically or create a separate MetaMask collateral policy.

## Canonical invocation

```bash
amb <subcommand> [args…]
```

The two scripts that cannot live on PATH use the absolute-path form:
```bash
node ${SKILL_DIR}/scripts/ride-relay.js <request_id>
node ${SKILL_DIR}/scripts/install.js
```

> **Output format:** Command output is human-readable text by default. The
> structured commands whose output you feed into a later command —
> `place-search`, `place-detail`, `map-session-verify`, `ride-pay-prepare`,
> `ride-search`, and all `coupon-*` commands —
> must be called with `--json` so you can reliably extract
> `placeId` / coordinates / `typed_data`. All other commands: read the plain text.

When re-favoriting or relabeling an existing local or history row, use `place-favorite` with its `id` or `dedup_key`.
Do not call `place-save` or send its Google Maps URL again.

## Available subcommands

| Area | Subcommand | Purpose |
|------|-----------|---------|
| **Wallet** | `wallet-status` | List registered wallets |
| | `wallet-setup --no-wait` | Create Privy wallet (always pass `--no-wait`) |
| | `wallet-setup-verify` | Check webapp auth status (after the user says they approved) |
| | `wallet-connect-metamask` | Connect or resume connection of a MetaMask Agent Wallet CLI account |
| | `wallet-sign` | Sign message (SIWE or typed data) |
| | `wallet-send-tx` | Send transaction |
| | `wallet-balance` | Wallet holdings as `balances[]` — one row per (chain, token), each naming its own `network`. Covers the payment chain, the bridge source chain, and deposit chains (MVL included). |
| **Deposit** | `deposit-status` | Check collateral status |
| | `deposit-add` | Deposit token collateral. Get the token address from `deposit-tokens`. Privy MVL goes direct; MetaMask MVL uses a `ROUTER_SIG` relay (cached JWT + one-time gas-paid approval); USDC uses the conversion relay. Relay paths block until confirmed (`--no-wait` to opt out). |
| | `deposit-relay-status` | Poll a gasless relay deposit by `request_id` |
| | `deposit-tokens` | List every depositable token for a network, MVL first, with addresses — the way to get the address `deposit-add` needs |
| | `deposit-withdraw` | Withdraw collateral as MVL. Privy uses sponsored gas; MetaMask submits `router.withdraw()` directly and pays native gas. A pending MetaMask approval resumes when the Agent reruns the same command. |
| | `bridge-deposit-eth` | Bridge ETH L1→L2 via L1StandardBridge (`amb bridge-deposit-eth <wallet_address> <value_eth> [recipient]`) |
| **Bridge** | `bridge-usdc` | Move Ethereum USDC → Base USDC via CCTP (`amb bridge-usdc <wallet_address> [amount] [--fast] [--wait]`). Amount is **decimal USDC** (`50`), unlike `deposit-add`. Omit the amount to resume. |
| | `bridge-usdc-status` | Read bridge job state (pure local read, no network) |
| | `bridge-usdc-quote` | What a bridge would cost and whether it is pre-approved, **starting nothing** (`amb bridge-usdc-quote <wallet_address> <amount> [--fast]`) |
| | `bridge-fast-grant` | Read / set / revoke the standing Fast-fee approval (`amb bridge-fast-grant <wallet_address> [<max_fee_usdc> \| --revoke]`) |
| **Member** | `whoami` | Report active account mode + identity |
| | `login --no-wait` | Start TADA/Throo member device-flow login (returns `approval_url`) |
| | `login-verify` | Complete login with the app's 4-digit code |
| | `logout` | Clear the active TADA/Throo member session |
| **Coupon** | `coupon-current` | List coupons the member still holds |
| | `coupon-past` | List used or expired coupons |
| | `coupon-detail` | Show one owned coupon |
| | `coupon-register` | Register a case-sensitive promotion code |
| | `coupon-available` | Find coupons valid for one route/product/card quote |
| **Auth** | `siwe-request-message` | Generate a Built-in Privy legacy SIWE message; never use for MetaMask login |
| | `siwe-submit` | Complete Built-in Privy legacy SIWE login |
| | `siwe-request-typed` | Generate the typed-data login challenge preferred for MetaMask |
| | `typed-submit` | Exchange a signed typed-data login challenge for the cached JWT |
| | `phone-verify-check` | Check phone verification status |
| | `phone-verify-start` | Send OTP |
| | `phone-verify-confirm` | Confirm OTP |
| **Setup** | `setup-check` | Check crypto-wallet ride readiness only; never use for member or undecided onboarding |
| | `install` | Initial installation |
| **Place** | `place-search` | Autocomplete place search |
| | `place-detail` | Get place coordinates |
| | `place-save` | Save a Google Maps URL as a frequent place (optional --label; on `APPROXIMATE_MATCH_NEEDS_FORCE` show the candidate and re-run with `--force` only after the user confirms — never same-turn) |
| | `place-list` | List saved places; `--match QUERY` (repeatable) for tier-per-pass union |
| | `place-remove` | Remove a saved place by id or label |
| | `place-favorite` | Promote history row → favorite (or relabel) by id or dedup_key |
| | `place-unfavorite` | Demote favorite → history; preserves hit_count |
| | `map-session-create` | Create map session |
| | `map-session-verify` | Poll map selection result |
| **Ride** | `ride-search` | Search available rides |
| | `ride-request` | Request a ride |
| | `ride-status` | Check ride status |
| | `ride-cancel` | Cancel ride — after driver assignment it returns `cancel_pending` + reasons instead of cancelling; the **rider** picks one, then re-run with `--reason-type <id>` (never pick for them) |
| | `ride-pay-prepare` | Prepare payment |
| | `ride-pay-confirm` | Confirm payment |
| | `ride-history` | List completed rides |
| | `ride-history-detail` | Get raw diagnostic detail; wallet: `<wallet_address> <request_id>`, member: `<request_id>` |
| | `ride-receipt` | Show the canonical Markdown receipt for a locally recorded `<request_id>` |
| | `ride-share <request_id> [--lang TAG]` | Shareable trip-tracking link (member + crypto). Use when the user asks to share their trip. |
| **Chat** | `chat-get-messages` | Get chat messages |
| | `chat-send-message` | Send message to driver |
| | `chat-send-image` | Send image to driver |
| **Tip** | `tip-config` | Get tip configuration for a region |
| | `tip` | Pay a tip for a finished ride (member: card; crypto: wallet) |

## Event streaming: ride-relay

Start ride-relay in the background once the ride is created and paid:
- **TADA member (`mode: "tada"`)** — card-paid: start ride-relay right after `amb ride-request` succeeds. Do **not** run `ride-pay-prepare`/`ride-pay-confirm` (wallet-only — they return `MODE_MISMATCH` for members).
- **Crypto (`mode: "wallet"`)** — start ride-relay after `amb ride-request` **and** `amb ride-pay-confirm` succeed.

Member vs crypto argument forms for `ride-search`/`ride-request`/`ride-status`/`ride-cancel` are in `references/ride.md` (`## Ride` → Member mode / Crypto mode). Run `amb whoami` to confirm `mode` before booking.

**Explicit member payment selection (DHL-30194):** read `references/member-payment.md` before a KH member booking, any request to use ABA account-on-file, or an explicit-method (`--payment-method`) member booking in another region. In KH, offer credit card or an already-linked ABA account; never silently switch methods. Elsewhere (NY, SG, HK) members pay by credit card only — an HK member may use either the unflagged card flow below or the v2 flow with `--region HK --payment-method CREDITCARD`. ABA_AOF is KH-only; never offer it outside KH. This explicit-source flow uses gateway v2, including v2 for credit cards. The existing unflagged member commands below remain the legacy card-only v1 flow; never mix their search IDs with v2. Crypto is separate and unchanged. TADA Wallet is not supported. Do not claim ABA staging payment has been verified merely because the client supports it.

**Member coupons:** follow `references/ride.md` → **Member coupons** for the canonical sequence. In brief: proactively find a coupon unless the user supplied a code or explicitly declined coupons; let the user choose a bookable product first; evaluate exactly the first **three** `available=true` candidates for that product in gateway order, or all candidates when fewer than three exist; re-quote each candidate and rank the exact quotes by lowest rider-facing price, preserving gateway order for equal prices. Present the winner first and show every successfully evaluated candidate's exact rider-facing price together with its code/title and discount metadata so the rider can choose. This is bounded product-first evaluation, not a global product × coupon minimum. Before `coupon-available`, never describe `available_coupon_count` from `ride-search` as the number of coupons applicable to the selected route/product; only `coupon-available` establishes that set. “Applied” means applied to the quote, not booked. Confirm before `ride-request`, pass the `search_id` from the final re-quote for the coupon the user selected, the selected `product_id`, the exact `coupon_code`, and the quoted `price` as `confirmed_price`; require `na=false`, `discount.applicable=true`, and an exact returned `discount.coupon_code`. A user-supplied code bypasses the three-candidate discovery cap. Requests to apply a coupon automatically, choose the best coupon, or choose the cheapest coupon all use this bounded explicit-code comparison; there is no separate server-side auto-apply path. Never use `campaign_promotion_code`, infer success from HTTP 200, or suggest changing away from card payment.

```bash
node ${SKILL_DIR}/scripts/ride-relay.js <request_id> [--agent <agent-id>] [--session-key <session-key>] [--session-id <sid>] [--once]
```

This is the invocation form for the flag reference below and for the
stdout-passthrough platforms (Claude Code Monitor, Hermes, codex/other) that run
ride-relay.js directly. **On OpenClaw, do not background this `node …/ride-relay.js`
form directly** — background the `ride-relay.sh` launcher instead (see the OpenClaw
row and "OpenClaw extra" below). A direct background launch is exposed to the
process-group startup race the launcher's `setsid` closes.

Flags by platform (see matrix below):
- **OpenClaw** takes no required identity flag. ride-relay resolves the agent and current session itself. `--agent`, `--session-key`, and `--session-id` remain optional compatibility/debug hints; do not invent them (see OpenClaw extra).
- **Hermes** requires `--once` so the relay self-exits after each batch and the agent can spawn the next one (agentic loop — see Hermes extra).
- **Claude Code / codex / other** take neither flag — ride-relay runs in stdout-passthrough mode until a terminal `ride_event` arrives.

`amb ride-request` has already self-spawned the detached monitor process, so ride-relay only consumes the event log and delivers events to the agent via the platform-appropriate primitive.

**Per-platform background spawn:**

| Platform | Env marker | Spawn primitive |
|----------|------------|-----------------|
| Claude Code | `CLAUDECODE` | `Monitor` tool running ride-relay as its `command` — each stdout `ride_event` line streams as a live notification; the relay self-exits on the terminal event, ending the watch |
| Hermes | `HERMES_SESSION_KEY` or `HERMES_HOME` | `terminal(background=true, notify_on_complete=true)` invoking ride-relay with `--once`; spawn the next relay on each completion notification (see Hermes extra) |
| OpenClaw | `OPENCLAW_SERVICE_MARKER` | background the **`ride-relay.sh`** launcher with `&` — it starts the relay in its own session (`setsid`) *before* Node boots, so OpenClaw's process-group teardown on tool-call return cannot kill it during startup; the command returns at once (printing a `RELAY_DETACHED` note with the child pid + log path). Pass only the request id; ride-relay resolves its agent id and live session itself (see OpenClaw extra) |
| codex / other | (unknown) | platform's own background primitive |

Common to all platforms: ride-relay self-exits when its work is done — by default (Claude Code / codex / OpenClaw) on a terminal `ride_event`; with `--once` (Hermes) after the first non-empty batch of events, terminal or not. The detached (OpenClaw) relay also self-exits if the ride monitor is gone and no event has arrived for 15 minutes, or after 4 hours in any case — so a stuck relay never lingers.

**Claude Code extra (loading the Monitor tool):** `Monitor` is a *deferred* tool — it must be loaded before it can be called, and a keyword search for it can miss. Use exact selection, then call it:

1. Load the tool with `ToolSearch` query `select:Monitor` (exact name — do **not** keyword-search `"Monitor"`; that can return "No matching deferred tools found" and lead you to a wrong fallback).
2. Call `Monitor` with the relay as its command and a long timeout:
   ```
   Monitor(
     description='<ride> status: <origin> → <dest>',
     timeout_ms=3600000,
     command='node ${SKILL_DIR}/scripts/ride-relay.js <request_id>',
   )
   ```
   Each stdout `ride_event` line then arrives as its own notification; the relay self-exits on the terminal event.
3. **Do not** fall back to a plain background `Bash` command for monitoring. A background `Bash` notifies only when the **process exits**, not per event line — intermediate status updates would never reach the user.
4. **Completion guard:** report the ride complete **only** when you have actually seen a terminal event line (`… the ride completed successfully` / `… reached terminal status FINISHED` / a cancel). A relay/monitor process merely *exiting* is **not** proof the ride finished — never infer completion from "background process completed". If the process ended without a terminal line, treat it as a dropped stream, not a finished ride.
5. On `FINISHED`, ride-relay outputs the completion prompt with a receipt offer and, only where the region supports tipping, a tip offer. Offer a tip only if the prompt carries one. It does not fetch the receipt. **Only when the user explicitly asks**, run `amb ride-receipt <request_id>` and surface stdout verbatim. Never reconstruct, translate, summarize, or reformat it.

**OpenClaw extra:** spawn ride-relay through the `ride-relay.sh` launcher, with the request id only:

1. Run (background it however you like — `&` is enough; the launcher returns at once):
   ```bash
   sh ${SKILL_DIR}/scripts/ride-relay.sh <request_id>
   ```
   The `.sh` launcher `exec`s the relay under `setsid` so it lives in its own
   session from the start — OpenClaw's group-kill on tool-call return cannot
   reach it. (Running `node …/ride-relay.js` directly still self-detaches, but
   only after Node has booted, leaving a startup window where the group-kill can
   land first; the launcher removes that window.)
2. ride-relay resolves its agent id via `openclaw agents list --json` (the sole configured agent, or the unique agent whose real workspace matches the inherited current directory). It lists that agent's active sessions and finds the unique transcript containing this ride request id. Missing or ambiguous correlation fails loudly; it never guesses the most recently updated session.

`--agent`, `--session-key`, and `--session-id` are retained for compatibility and debugging. If supplied, they are validated against deterministic resolution; a stale or fabricated hint may be corrected only when the transcript/workspace result is unique, while a conflict between two valid identities fails closed. Normal agent behavior must not call `session_status` or invent identity flags for ride-relay.

ride-relay automatically detects whether any messaging channel is configured (via `openclaw channels list`):
- channel configured → deliver pushes to the channel **and** appends into the resolved session (`--channel last --deliver --session-id <resolved-sid>`),
- no channel → deliver appends into the resolved session only (still inject; no channel push).

Either way the LLM sees `ride_status` events as user-turn messages inside the session ride-relay resolved.

**Hermes extra (agentic relay loop):** Hermes does not have an in-session deliver primitive like OpenClaw. Instead, when a background process completes, Hermes injects a synthetic `[IMPORTANT: Background process … completed. Output: …]` user-turn message on the next agent turn — that is how the relay's stdout reaches the agent. ride-relay self-exits after each batch with `--once`, and you spawn a new relay each turn until terminal status.

1. At the mode-specific commit point — after a successful `amb ride-request`
   for a member ride, or after `amb ride-pay-confirm` succeeds for a crypto
   ride — spawn the first relay:
   ```
   terminal(
     command='node ${SKILL_DIR}/scripts/ride-relay.js <request_id> --once',
     background=true,
     notify_on_complete=true,
   )
   ```
   Reply briefly to the user ("monitoring ride status…") and end the turn.

2. When a turn opens with a `[IMPORTANT: Background process … completed. Output: …]` notification, parse the embedded `TADA ride … status …` line (or `… reached terminal status …` for terminal events) and **report that status line to the user verbatim** — do not paraphrase, the exact wording is part of the ride record. On `FINISHED`, offer an on-demand receipt, and offer a tip **only when the relayed line itself carries a tip amount** — some regions have no tip support, and their completion line has none. Never invent a tip offer. Do not show or fetch the receipt body unless the user asks. Then:
   - **non-terminal status** → spawn another ride-relay with the same options.
   - **terminal status** (`reached terminal status FINISHED` / `USER_CANCELED*` / `DRIVER_CANCELED*` etc.) → stop the loop, do NOT spawn another relay.

3. **Fallback** (harness modes without automatic process-completion injection — e.g. an ACP-driven test harness): If a turn starts and you have a previously-spawned ride-relay but no `[IMPORTANT: …]` notification has arrived, proactively call `process(action='list')` to find exited processes, or `process(action='poll', session_id=<saved-relay-session-id>)` on the saved relay session id. Treat the captured stdout the same way as the `[IMPORTANT: …]` notification — parse + report verbatim + spawn the next relay if non-terminal.

   - **Paging args caveat for `process(action='log')`**: when you fall back to `process(action='log', session_id=<id>)`, **omit the `offset` and `limit` arguments entirely** — the defaults (offset=0, limit=200) give the last 200 lines of stdout. Passing `limit=0`, `offset=1`, or any combination that slices to an empty range returns `{"output": "", "total_lines": N, "showing": "<X> lines"}` with `output=""` even when the process emitted text. Prefer `process(action='poll', …)` for short single-line relay output — its `output_preview` field (last 1000 chars of stdout) carries the full `TADA ride … status …` line for a one-shot --once relay.

For the full event schema, reconnect procedure, exit-code semantics, and related details, see the ride-relay section of `references/ride.md`.

**Diagnosing a monitoring failure (dev/staging only):** If ride status or driver-chat events aren't reaching the session, run `amb debug <request_id>`. It creates a local `~/.amb/debug/tada-debug-*.zip` containing monitor/event/relay logs, process locks, cursors, and a summary. The collector's source-path whitelist excludes `state/data/.env`, `state/keys/`, and SQLite database files (including WAL/SHM files). It does **not** redact the included logs: they can contain pickup/drop-off, timestamps, ride/account identifiers, driver details, chat, or any sensitive value already written to a collected log. (The command is not available in prod builds.)

**Do not send that zip anywhere unless the user explicitly asks after being told its exact path and the data classes above.** Recommend that they inspect and redact it first. If they still ask you to share it, name the destination and the unredacted-content risk before doing so; the destination's own access and retention policy applies.

### Out-of-band ride alarms (optional)

By default a Flavor A harness (Claude Code, codex, Hermes, …) surfaces ride
status through the agent's own context. To also push alarms out-of-band —
so the user is notified even when they are not watching the session — set any
of these environment variables; the relay fans out to every configured sink:

- `AMB_RIDE_NOTIFY_WEBHOOK_URL` — POST each alarm as JSON to this URL.
- `AMB_RIDE_NOTIFY_WEBHOOK_SECRET` — optional; when set, the body is signed
  `X-Amb-Ride-Signature: sha256=<hmac>` so the receiver can verify it.
- `AMB_RIDE_NOTIFY_TELEGRAM_BOT_TOKEN` + `AMB_RIDE_NOTIFY_TELEGRAM_CHAT_ID` —
  push straight to a Telegram chat via the third-party Telegram Bot API.

Webhook JSON and Telegram messages contain the rendered ride alarm. Depending on
the event, that text can expose ride status, driver/vehicle details, driver chat,
or a live tracking link to the configured third party. Review the destination and
its access/retention policy before enabling a sink. The webhook HMAC secret and
Telegram bot token authenticate delivery and are not included in the alarm body.

When a sink delivers an event, the in-band line is marked context-only so the
agent does not double-notify; if every sink fails, the agent notifies in-band
as a fallback. Under OpenClaw, a session with a resolvable channel target
(e.g. a Telegram-born session) always has its native channel as a sink, and
these vars add extra destinations on top. Sessions with no derivable channel
target (CLI/API-launched, operator TUI) fall back to in-band-only delivery
regardless of these vars.

## Member ride: card payment auto-resolution

When the active mode is `tada` (TADA/Throo member), `payment_item_uuid` (in `ride-request`) and `card_uuid` (in `ride-search`) are **optional**. The CLI resolves the payment card automatically:

- **0 cards / all expired** → error `NO_CARD`. Tell the user to add a card in the TADA/Throo app and try again. Cards are looked up on the pickup's regional gateway, so if the user insists a card is already saved, re-check the coordinates you passed before asking them to add another one.
- **1 non-expired card** → that card is auto-selected; no agent action needed.
- **2+ non-expired cards, exactly one with `is_default`** → the default is auto-selected; no agent action needed.
- **2+ non-expired cards, no single default** → the command returns:
  ```json
  {
    "needs_card_selection": true,
    "cards": [...],
    "next_action": "ASK_USER_TO_PICK_CARD_THEN_RERUN_WITH_payment_item_uuid"
  }
  ```
  Show the card list to the user, ask them to pick one, then re-run `ride-search` / `ride-request` with the chosen card's `id` as `card_uuid` / `payment_item_uuid`.
- **Card lookup fails (gateway error or expired session)** → error `CARD_LOOKUP_FAILED`. Retry or ask the user to check connectivity / re-authenticate.

Do **not** call `GET /v1/cards` yourself — the CLI handles it internally. For card details (fields, expiry semantics, is_default meaning), see `references/ride.md` → "Card resolution".

## Member ride: place resolution

When the active mode is `tada` (TADA/Throo member) and the user names a place, asks to go "near me", or mentions an airport, resolve the destination/origin with the gateway place commands before building ride locations:

- **Named place** → `amb place-search <query> <region> [originLat originLng] --json`. Present the list; if the selected result has `lat_lng: null` (Google candidate), run `amb place-detail <place_id> <region> --json` to get coordinates.
- **Near me / nearby pickup** → `amb place-nearby <lat> <lng> --json` (TADA POIs only; requires user's current coordinates).
- **Airport / terminal** → `amb place-airports <city> --json` (e.g. `amb place-airports NYC`).
- **Coordinates only** → `amb place-reverse-geocode <lat> <lng> <region> --json` to convert to a named place.

Region whitelist is currently **NY**, **SG**, **KH**, and **HK**; any other value returns an error.

After resolving: copy `place_id`, `lat_lng.{latitude,longitude}`, `name`, and `address` verbatim into the ride `LocationRequest` — never fabricate or alter these values. For airports/terminals with `sub_places`, ask the user to pick the Pickup (`allowance_type 1`) or Dropoff (`allowance_type 2`) sub-point and book using `sub_place_id` + that sub_place's coordinates.

For the full command signatures, field reference, and resolve→ride flow, see `references/ride.md` → "Member place search".

## USDC bridge

Crypto-mode rides settle in **Base USDC only**, so a user holding USDC on Ethereum can be unable to pay. Two paths move it, and they are not interchangeable.

**When the user asks where an existing bridge transfer stands, first run `amb bridge-usdc-status <wallet_address>`.** This is a read-only local-state check and is the authoritative source for the skill's locally tracked bridge jobs. Never substitute Etherscan, BaseScan, or another public explorer: chain history cannot reconstruct the local job state, relay progress, or recovery contract.

**A status/check-only request is not permission to resume a bridge.** Report the observed state and the safe next action without running `bridge-usdc`, even if status output supplies a resume command. A resume hint is an available recovery path, not an instruction to execute during a status check. Resume only when the user asks to resume/continue, or when an already-authorized ride workflow requires finishing its pending bridge. Do not turn “check again” into a mutation.

For `BURN_SUBMITTED`, describe the source burn only as submitted, never complete or confirmed. Do not paraphrase it as `burn done`, `burn confirmed`, or `one step is done`; the whole bridge remains in progress until `COMPLETED`. Keep stage completion distinct from transfer completion even when the response also names the remaining attestation and mint steps.

**Top-up — the normal path. Offer it right after a ride ends.**

After the user explicitly requests and sees the canonical receipt, use `amb ride-history-detail <wallet_address> <request_id> --json --account=wallet` for the top-up calculation. Compare the payment-chain USDC balance against `receiptInfo.paidAmount` only when `receiptInfo.paidCurrency` is exactly `USDC`; if either field is absent, skip the offer. Do not fetch receipt data merely to make a top-up offer. If settlement is pending, wait for a later explicit receipt request.

**Do not use `receiptBreakdown[].totalFare`.** The same receipt carries the fare a second time in fiat (e.g. `29.19 USDC` alongside `37.06 SGD`), and the two are close enough that picking the wrong one looks reasonable and is silently wrong.

If the balance is now below that fare, the user cannot take the next ride without waiting. Offer to top the wallet back up to about three rides' worth with a Standard transfer: **no fee, ~20 minutes**.

The amount to move is `fare × 3 -` the payment-chain USDC row, not `fare × 3` — the wallet keeps what is already in it. Clamp to what the bridge source chain's USDC row can cover including the fee. Tell the user the figure and get their agreement before sending it.

Do not promise "ready in 20 minutes". A Standard transfer submits the burn and returns; the server relayer attempts to continue through attestation and mint, with the same-job CLI resume as fallback.

**Always ask before topping up.** A Standard quote reports `preauthorized: true` because its fee is zero — that means *the fee needs no approval*, not that the transfer does. Moving a user's money at a moment they never asked to travel requires their agreement to the amount.

**An explicit Standard instruction is already approval.** A direct instruction to move an exact amount using Standard is the user's transfer approval. You may inspect readiness or quote first, but do not stop after `bridge-usdc-quote` to ask for the same approval again: run `amb bridge-usdc <wallet_address> <amount>` in that same turn unless the quote or readiness result blocks the transfer. This does not authorize a different amount, Fast mode, a fee, or a replacement transfer.

**Express — only when they need to ride now.**

**Move only the shortfall.** The shortfall is what the wallet is *missing*, never what the next command will spend:

- **Ride payment** — `fare - usdc`. The fare is `price` from `ride-search`, already in the pay currency.
- **`INSUFFICIENT_DEPOSIT`** — `requiredToActivate[].tokenWei` **converted from raw** (USDC has 6 decimals) is how much `deposit-add` will spend, **not** the shortfall. Subtract what the wallet already holds: `max(0, that amount - usdc)`. A wallet holding 3 USDC that needs a 4 USDC deposit is short 1, not 4 — bridging 4 would move three times more than this ride requires.

Do not top up to three rides' worth here. The user agreed to take a ride; they did not agree to move a larger sum out of Ethereum. **Anything above the shortfall needs their word** — offer it, don't assume it. Topping up in bulk is the other path's job, and that path always asks.

Then `amb bridge-usdc-quote <wallet> <shortfall> --fast`. If it reports `below_min: true`, raise the amount to `min_usdc` — that is the smallest transfer the bridge accepts, so it is not a discretionary increase. If it reports `sufficient: false`, the source cannot cover even the shortfall: report that and stop, rather than retrying at a smaller amount that would not fix anything.

**Confirm the transfer before you run it, every time.** Say the amount, the chains it moves between, and the fee, then wait for the user's word. `preauthorized: true` means they set a standing ceiling for the *fee* — it is not agreement to move this sum now, and treating it as such spends their money on a decision they did not make. When `preauthorized` is `false`, the fee needs its own approval too, so ask for both and offer the free 20-minute option alongside. Report the amount and the actual fee once it completes (~40 s, blocking).

**The CLI backs this up.** `bridge-usdc --fast` refuses with `BRIDGE_FEE_NOT_AUTHORIZED` when the fee it computes is not covered by a standing approval, so skipping the quote does not skip the ceiling, and a fee that grew since you quoted is refused rather than spent. Standard is unaffected — its fee is zero.

That check is a guard against *drift*, not a security boundary: `bridge-fast-grant` is an ordinary command, so nothing stops an agent from raising its own ceiling first. What the gate buys is that spending a fee has to be a deliberate, recorded act instead of an incidental one. **Asking the user is still your job.**

After the bridge lands, **retry the command that failed**: `deposit-add` then the ride request for `INSUFFICIENT_DEPOSIT`, or the payment/tip for `INSUFFICIENT_BALANCE`. Bridging alone does not fill collateral.

**Read `preauthorized`; never compare fees yourself.** The ceiling lives in `amb bridge-fast-grant` and the comparison is the CLI's job.

**Before every ride, finish what is pending.** If `amb bridge-usdc-status <wallet>` shows an unfinished job, run `amb bridge-usdc <wallet>` (no amount) to resume. A single resume often closes the job outright now: the server finishes Standard transfers on its own, and the CLI checks whether the transfer already arrived before sending anything. If it returns `MINT_SUBMITTED`, the CLI sent the mint itself and is waiting for it to confirm — wait ~5 seconds and resume again, up to twice more. If it still has not completed, **do not count that money as available** — and do not offer an express bridge either, because an unfinished job blocks a new one (`BRIDGE_JOB_IN_FLIGHT`). Tell the user the top-up is finishing and to try again shortly.

**If quoting fails, it depends which path you are on.** After a ride (top-up), drop the offer silently and carry on with the receipt — a fee-service outage must never cost the user their ride summary. Before a ride (express), report the failure and **do not proceed** with the ride, payment, or tip: the balance is still short.

`amb bridge-usdc` moves Ethereum USDC to Base USDC (crypto-mode rides settle in Base USDC only). A Standard transfer takes ~20 minutes and does **not** block, so most `bridge-usdc` calls return while the money is still in flight.

> **Only `status: COMPLETED` means the bridge is done.** Any other status — `INITIATED`, `BURN_SUBMITTED`, `ATTESTED`, `MINT_SUBMITTED` — means it is still in progress. **Never tell the user their top-up succeeded.** A completed Fast job may carry `minted_amount_unknown: true`: the USDC arrived, but the exact credited amount could not be read. Preserve `minted_amount_note` and use `amb wallet-balance <wallet_address>` to verify the current balance; do not call that null amount a failed bridge.

After starting or resuming a non-terminal bridge, report the decimal amount and symbol, name both source and destination chains, and distinguish burn submission, attestation waiting, and the server relay's future mint. Never call `INITIATED` or `BURN_SUBMITTED` complete. Tell the user to check the existing job instead of starting the transfer again, and never expose raw base units.

For every non-terminal bridge response, surface every `agent_guidance` obligation in the user-facing response: current stage, server continuation, check-later path, same-job CLI fallback, and the prohibition on starting a new transfer. Concretely, preserve `current_stage`, explain `remaining_stages`, describe `completion_mode: SERVER_RELAY_WITH_CLI_FALLBACK`, follow `user_action_required: CHECK_STATUS_LATER`, provide the read-only `status_command`, use the same job's `next_step` as the fallback, and honor `do_not_start_new_transfer`. Translate identifiers into the user's language, but never infer or report a later stage than `current_stage`.

Before ending that turn, repeat both `status_command` and `next_step` verbatim from the same CLI response, and label both commands as operating on the same existing job. Do not paraphrase either command away. The first is the read-only check-later path; the second is the fallback that resumes that job without an amount. This explicit binding prevents a user from mistaking the fallback for permission to start a replacement transfer.

When you report an in-progress bridge, tell the user **how it finishes**, not only that it is unfinished: the server relayer attempts it in the background; the user should check the existing job later, and if it remains pending the same-job `next_step` resume is the fallback. That resume is not a new transfer. A ~20-minute Standard transfer that you report as merely "not complete", with no word on how it resolves, leaves the user unsure it will ever land.

A blocking call that times out is not an error — it exits 0 carrying the live status. Report that status as in-progress and continue with `amb bridge-usdc <wallet_address>` (no amount) to resume; every unfinished response names that command in `next_step`.

**`FAILED` with `funds_mid_flight: true`** is the one terminal state where the USDC is on neither chain — burned on Ethereum, not yet minted on Base. That response carries a `recovery` text. **Surface that text to the user verbatim, do not paraphrase it.** The job exists only in this machine's local SQLite; no server can reconstruct it, so the user's `bridge-usdc-status` output is the sole recovery input support will ever have. Nothing is lost, but only that output can finish the transfer.

Amounts are **decimal USDC** (`50`, `50.5`) — unlike `deposit-add`, which takes raw 6-decimal units (`50000000`). Every bridge response carries both `amount_usdc` and `amount_raw`; check them against what you meant to send. On `--fast` the amount is what the user **receives** — the burn is larger by the max fee.

Full command surface, wait behaviour, and error codes → `references/wallet.md` → "USDC Bridge".

## Ride receipt

After `FINISHED`, fetch a receipt only when the user explicitly asks:

```bash
amb ride-receipt <request_id>
```

Surface stdout verbatim. `RECEIPT_NOT_READY` means settlement is pending; ask
the user to try again shortly. The local ride selects member or wallet mode.
Wallet receipts include payment, refund, and paid-tip transaction links. Full details:
`references/ride.md` → "Ride History".

## Per-feature references

- Wallet management, SIWE login, phone verification, balance check, collateral, USDC bridge → `references/wallet.md`
- Place search, saved places (local catalog + Step 0 lookup), ride booking/status/cancellation/payment, ride history → `references/ride.md`
- Driver chat (messaging + image) → `references/chat.md`
- Tip configuration and payment → `references/tip.md`
- User-facing questions about the skill (purpose, FAQ, walkthrough) → `references/usage.md`

## Error Handling

When an `amb <subcommand>` fails, check the error code and take corrective action. Error code → action table: see the Error Handling section in `references/ride.md`. For an unknown error in wallet mode during a crypto ride, run `amb setup-check <wallet_address>` to diagnose crypto readiness. Do not use `setup-check` for member-mode or account-unselected errors; diagnose those from member authentication state and the failing command instead.

When `install.js` itself fails (before any `amb` command runs), it writes a single-line JSON to stderr: `{"error":"<CODE>","message":"..."}`. Possible codes: `SSH_KEY_MISSING`, `SYMLINK_FAILED`, `PATH_MISSING`, `SHA_MISMATCH`, `VERSION_MISMATCH`, `AMB_INSTALL_FAILED`. See the **Install error codes** section in the skill's `README.md` for the per-code recovery action. `install.js` is idempotent — re-run after fixing.
