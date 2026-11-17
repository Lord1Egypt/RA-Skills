# Wallet & Authentication Reference

> All agent-facing operations use `amb <subcommand> [args…]` (PATH-resident). Two scripts that cannot live on PATH (`ride-relay.js`, `install.js`) are invoked via `node ${SKILL_DIR}/scripts/<name>.js` — see `../SKILL.md` for the path convention.

## Signing Strategy

Crypto-mode users sign with their selected registered wallet. The built-in Privy wallet's
legacy SIWE path uses `personal_sign` (Privy-only):

```bash
amb wallet-sign <address> personal_sign <siwe_file>
```

Wallet setup is optional. Enter it only when the user chooses crypto payment or explicitly
asks for a wallet-dependent feature; member login and card-paid rides do not need a wallet.
When a wallet is first needed, offer **Built-in Privy
(recommended/default)** or **MetaMask**. `privy` is the built-in embedded wallet provisioned by
`wallet-setup`. `metamask` is an external wallet driven through the MetaMask Agent Wallet CLI
(`mm`), registered with `wallet-connect-metamask`; the skill never sees its keys and asks `mm`
for every signature. Use Privy when the user has no preference.

The Agent runs `amb wallet-connect-metamask` for a MetaMask choice; never tell the user to run
an `amb` command. When the command returns `status: "approval_pending"`, ask the user only to
complete the external MetaMask approval and end the turn. After confirmation, the Agent runs
the identical `amb wallet-connect-metamask` command again. The command resumes its private
mode-0600 state automatically and deletes that state after registration or a definite terminal
result; pending or indeterminate results remain resumable. Never expose or manually
use an mm polling ID. After registration, the Agent runs typed login in order: `amb siwe-request-typed <wallet_address> <chain_id>` → `amb wallet-sign <wallet_address> eth_signTypedData_v4 <typed_file>` → `amb typed-submit <typed_file> <signature>`.

Use the literal wallet address returned by `amb wallet-status --json` directly in both
`siwe-request-typed` and `wallet-sign`. Do not use a shell variable or command substitution for that address.

For typed-sign approval recovery, follow the exact-command contract in
[`wallet_sign`](#wallet_sign---sign-a-message) below; it applies to both login and payment.

Older installs may still hold a wallet of type `external`, registered by the retired
`wallet-add-external` command. The skill cannot sign for those. Re-register with
`wallet-connect-metamask`.

A MetaMask wallet pays its own gas for the one-time `approve` before its first MVL deposit and
for a direct collateral withdrawal. Depositing USDC needs no gas.

Check wallets:
```bash
amb wallet-status
# If multiple wallets exist, ask the user which one to use
```

## Wallet Management

### wallet_setup - Initialize wallet

```bash
# Agent invocation — ALWAYS use --no-wait
amb wallet-setup --no-wait [--force-new]
```

Creates the user's built-in Privy wallet, or checks the status of an existing one. Run it after
the user selects the recommended/default Privy option during wallet onboarding.
- `--no-wait`: **Required for agent use.** Returns the JSON contract (`auth_required` / `auth_pending` with `auth_url`, or `ready`) and exits immediately, so the agent can show the URL to the user. Without this flag the command blocks for up to 5 minutes waiting for a human at a terminal to finish webapp auth — an agent cannot drive that.
- `--force-new`: Create a new wallet even if one already exists

### wallet_status - List wallets

```bash
amb wallet-status
```

Returns all registered wallets and their validity status.

**If there are 2 or more wallets, always ask the user which one to use. Never choose arbitrarily.**

### wallet_check_auth - Check auth status

```bash
amb wallet-setup-verify [--wait]
```

Checks whether webapp authentication is complete. Returns one of `no_pending` / `pending` (with `auth_url`) / `ready` (with `wallet_address`) / `failed`.

- Default: **one check, returns immediately.** This is the agent path.
- `--wait`: block for up to 5 minutes, polling until the approval lands. Only for a human at a terminal.

**Send the `auth_url` to the user and end your turn before verifying.** The user only sees a message once your turn ends, so an unsent link cannot be opened — verifying (or waiting) in the same turn that produced the link means waiting for an approval the user has no way to give. Send the link, stop, and run `wallet-setup-verify` once the user says they finished the page. Re-run it on request rather than polling it in a loop.

**When presenting `auth_url`:** always use a markdown hyperlink so the user can click it directly:
```
[Authenticate here](auth_url_value)
```
Never display the raw URL as plain text — it is long and wraps in the terminal, making it impossible to copy correctly.

### wallet_sign - Sign a message

```bash
amb wallet-sign <wallet_address> <sign_method> <siwe_file|typed_file|typed_data_json>
```

The third argument depends on `sign_method` — it is **not** a raw message string:
- `personal_sign` → Built-in Privy SIWE re-auth only. Pass the **`siwe_file` path** returned by `amb siwe-request-message`: `amb wallet-sign <wallet_address> personal_sign <siwe_file>`. Do not use this for MetaMask login.
- `eth_signTypedData_v4` → for MetaMask login, pass the **`typed_file` path** returned by `amb siwe-request-typed`: `amb wallet-sign <wallet_address> eth_signTypedData_v4 <typed_file>`. For ride/tip payment, pass the inline typed-data JSON: `amb wallet-sign <wallet_address> eth_signTypedData_v4 '<typed_data_json>'`.

For MetaMask, an `approval_pending` result is not a reason to submit again. After the user
completes external approval, rerun this exact command; its private mode-0600 state resumes the
same address-scoped request automatically. Address/method/input/parsed-data mismatch preserves
the pending request and fails closed; only the exact expired typed file may clear its stale state.
Pending/indeterminate remains resumable, while success or any terminal result clears it. Never
expose polling internals or ask the user to run `amb` or `mm`.

If a MetaMask command reports a coded `*_RESUME_INVALID` error, it names only the
affected resume file. Do not delete that file or start a fresh request automatically.
An operator must reconcile the matching mm request without exposing its credential or
polling ID: preserve the file while the request is pending or indeterminate, and remove
it only after confirming that the request is terminal or absent.

### wallet_send_tx - Send transaction

```bash
amb wallet-send-tx <wallet_address> <to> <value_eth> <chain_id> [data]
```

## Built-in Privy SIWE Authentication

This legacy SIWE flow is for Built-in Privy. MetaMask login uses only the typed-login sequence
documented above; if its signature is pending, rerun the exact same `wallet-sign` command after
the user approves it.

### siwe_get_message - Generate SIWE message

```bash
amb siwe-request-message <wallet_address> <chain_id>
```

Saves the message under the Ambient state data directory and returns the `siwe_file` path.

### siwe_login - SIWE login

```bash
amb siwe-submit <siwe_file> <signature>
```

- `siwe_file`: File path returned by `amb siwe-request-message`
- JWT is saved to DB and reused by subsequent commands.

## Phone Verification

**Always follow this order.**

1. Get the phone number from the user (E.164 format, e.g. +821012345678)
2. Run `amb phone-verify-check` to check verification status on the server
   - `verified: true` → Saved to local DB, done. No OTP needed
   - `verified: false` → Proceed to step 3
3. Send OTP with `amb phone-verify-start`
4. Get OTP code from user and confirm with `amb phone-verify-confirm`

### phone_verify_check - Check server verification status (always run first)

```bash
amb phone-verify-check <wallet_address> <phone>
```

### phone_verify_start - Send OTP (only when phone_verify_check returns verified: false)

```bash
amb phone-verify-start <wallet_address> <phone>
```

### phone_verify_confirm - Confirm OTP

```bash
amb phone-verify-confirm <wallet_address> <phone> <code>
```

## Balance Check

### balance_check - Check wallet balance

```bash
amb wallet-balance <wallet_address>
```

Returns what the wallet actually holds (not the deposit contract balance). One row per (chain, token):

```json
{
  "wallet_address": "0x681D…",
  "balances": [
    { "network": "BASE",     "symbol": "ETH",  "amount": "0" },
    { "network": "BASE",     "symbol": "USDC", "amount": "12.5",  "address": "0x8335…" },
    { "network": "ETHEREUM", "symbol": "ETH",  "amount": "0" },
    { "network": "ETHEREUM", "symbol": "USDC", "amount": "310",   "address": "0xA0b8…" },
    { "network": "ETHEREUM", "symbol": "MVL",  "amount": "40000", "address": "0xA849…" }
  ],
  "errors": []
}
```

Every row names its own chain, so never assume which chain a balance is on. Which network plays which role depends on the build — on production, rides are paid in USDC on `BASE` while collateral and bridging live on `ETHEREUM`.

- `address` is **absent on native rows**, and that absence is what marks a row as the chain's native coin. Token rows always carry the contract address — including MVL, so this output is one place to get the address `deposit-add` needs.
- `amount` is a decimal string with no padding: `"0"`, `"12.5"`, `"40000"`. Do not expect a fixed number of decimal places.
- Rows are ordered payment chain first, then the bridge source chain, then deposit chains; within a chain, native → USDC → MVL.

- `errors`: rows that could not be read, as `{ network, symbol, error }`. Reads are isolated per row, so one unreachable chain or one failing token lookup never suppresses the others — the healthy rows still appear in `balances`.

**Three situations look similar and mean different things. Do not conflate them:**

| Situation | Meaning | What to tell the user |
|---|---|---|
| Row present, `"amount": "0"` | Configured, read fine | They hold none of it right now. |
| Row absent **and** listed in `errors` | Configured, but the read **failed** | A temporary lookup problem — the balance is unknown, not zero. Retry. |
| Row absent **and** not in `errors` | That (chain, token) pair is **not configured in this build** | The capability is unavailable here — not a balance problem. |

So check `errors` before concluding anything from a missing row. If no `ETHEREUM` rows appear and `errors` is empty, this build genuinely has no bridge and no Ethereum deposit chain. If they are missing because they are in `errors`, saying "bridging is unavailable" sends the user to the wrong fix — and reporting an unknown balance as `0` is just as bad.

## USDC Bridge (Ethereum → Base)

Crypto-mode ride payment settles in **Base USDC only**, but USDC liquidity lives on Ethereum, so a user can hold plenty of USDC and still be unable to pay for a ride. `bridge-usdc` moves Ethereum USDC to Base USDC over Circle CCTP V2. The user needs **no gas token on either chain** — gas is sponsored on both sides.

**When to use it:** two situations, handled differently — see SKILL.md → "USDC bridge". In short: a **Standard** top-up right after a ride ends (free, ~20 min, always ask), and a **Fast** transfer when the user needs to ride now (small fee, ~40 s, skip the fee question when `bridge-usdc-quote` reports `preauthorized: true`).

### bridge_usdc - Start or resume a bridge

```bash
amb bridge-usdc <wallet_address> <amount> [--fast] [--wait]   # start
amb bridge-usdc <wallet_address>                              # resume
```

#### Amount units — decimal USDC, NOT raw

`bridge-usdc` takes **decimal USDC** (`50`, `50.5`). `deposit-add` takes **raw** 6-decimal units (`50000000`). The divergence is deliberate — an agent producing `50` is far safer than one producing `50000000` — but the two commands sitting side by side is a live confusion risk.

```bash
amb bridge-usdc 0xabc… 50        # 50 USDC   ✅
amb bridge-usdc 0xabc… 50000000  # 50 million USDC — rejected by the balance check, not by the parser
```

Because of that risk **every `bridge-usdc` response carries both `amount_usdc` and `amount_raw`**. Read them back and confirm they match what you meant before reporting anything to the user.

Amounts finer than 6 decimal places are rejected (`BRIDGE_AMOUNT_INVALID`), never rounded — `50.1234567` would silently become a different amount than the user authorized.

#### The amount is what you RECEIVE, not what is burned

- **Standard**: `maxFee` is 0 → `bridge-usdc <wallet> 50` burns exactly 50 and delivers exactly 50.
- **`--fast`**: `bridge-usdc <wallet> 50 --fast` burns **`50 + maxFee`** and delivers **at least 50** (the real fee is usually below the authorized max, so slightly more can arrive).

The pre-flight balance check is against `amount + maxFee` for the same reason. When it fails, `BRIDGE_INSUFFICIENT_USDC` spells out both parts.

#### Standard vs `--fast`

| Mode | Fee | Time | Blocks? |
|---|---|---|---|
| Standard (default) | none | ~20 min | **No** — returns as soon as the burn is submitted |
| `--fast` | small — Circle quotes it at call time (~1 bps) | ~40 s | **Yes**, up to 3 min |
| Standard + `--wait` | none | ~20 min | Yes, up to 25 min |

Standard does not block by default because a 20-minute blocking call is unusable for an agent. It returns a non-terminal status plus `next_step`; resume later. `--wait` opts Standard into blocking — only use it if a human is genuinely waiting at a terminal.

A blocking call that hits its timeout is **not a failure**. It exits 0 with the live status: the funds are mid-flight and Circle attests regardless of whether anyone is polling. Resume it.

#### Resuming

```bash
amb bridge-usdc <wallet_address>
```

Calling `bridge-usdc` with **no amount** picks up the wallet's unfinished job and advances it as far as it can. It is idempotent and is the normal way to continue — this is the one command to remember. Every unfinished response names it in `next_step`.

When you report an unfinished bridge to the user, say **how it finishes**, not just that it is unfinished: the server relayer attempts to continue through attestation and mint, with the same-job CLI resume as fallback. Tell them to check the existing job later and use its `next_step` only if it remains pending. Reporting only the status leaves them unsure a non-blocking Standard transfer will ever land.

Only one bridge per wallet may be in flight; starting a second one fails with `BRIDGE_JOB_IN_FLIGHT`. There is no `--force` override, and none is needed: resuming resolves a stuck job on its own.

If another process is already advancing the job, the command returns immediately with `lease_held: true` rather than blocking.

### bridge_usdc_quote - Price a transfer without starting one

```bash
amb bridge-usdc-quote <wallet_address> <amount> [--fast]
```

A pure read: one fee lookup, one balance read, one local lookup. **It never creates a job**, so it cannot consume the wallet's single in-flight slot.

```json
{
  "amount_usdc": "90", "amount_raw": "90000000",
  "mode": "standard",
  "max_fee_usdc": "0", "max_fee_raw": "0",
  "required_usdc": "90",
  "source": "ETHEREUM",
  "source_balance_usdc": "282",
  "sufficient": true,
  "below_min": false, "min_usdc": "1",
  "preauthorized": true,
  "grant_max_fee_usdc": "0.1"
}
```

- `sufficient` — whether the USDC balance on the bridge source chain (the `ETHEREUM`/`USDC` row of `wallet-balance`) covers `amount + max_fee`. **Not an error**: a shortfall is an answer to the question you asked. Shrink the amount and quote again if you want.
- `below_min` — below the build-configured minimum bridge amount. Also a field, not an error. Starting such a transfer *is* refused (`BRIDGE_AMOUNT_BELOW_MIN`), but asking about it is not.
- `preauthorized` — whether this transfer's fee is already approved. **Read this instead of comparing fees yourself.** Standard is always `true` (a zero fee has nothing to approve), which is about the fee only — it is never consent to move the money.
  The same check runs inside `bridge-usdc --fast` and refuses with `BRIDGE_FEE_NOT_AUTHORIZED`, so this field tells you what *would* happen rather than being the only thing standing between the fee and the wallet. That is a guard against drift, not a security boundary — `bridge-fast-grant` is an ordinary command, so raising the ceiling is one call away. Asking the user remains the caller's job.

### bridge_fast_grant - Standing approval for Fast fees

```bash
amb bridge-fast-grant <wallet_address>                    # read
amb bridge-fast-grant <wallet_address> <max_fee_usdc>     # set
amb bridge-fast-grant <wallet_address> --revoke           # clear
```

All three return the same shape; branch on `granted`:

```json
{ "wallet_address": "0x…", "granted": true,
  "max_fee_usdc": "0.1", "max_fee_raw": "100000",
  "granted_at": "2026-07-21 04:12:00" }
```

The grant does not expire; it lasts until revoked. Ask for it the first time an express bridge is actually needed — never during setup, where the user has no context for the question. It is scoped to one wallet.

`BRIDGE_GRANT_INVALID` means either the ceiling was not a decimal USDC amount, or `--revoke` was combined with an amount. Nothing was stored or cleared in either case — a consent command does not guess which operation you meant.

### bridge_usdc_status - Read bridge job state

```bash
amb bridge-usdc-status <wallet_address> [job_id]
```

A **pure local read** — no network, no wallet registration needed, no side effects (same contract as `deposit-relay-status`). With `job_id` it returns that one job; without it, every job for the wallet plus `active_job_id`.

### Response fields

Both commands render a job the same way:

| Field | Notes |
|---|---|
| `job_id`, `status`, `wallet_address` | |
| `amount_usdc`, `amount_raw` | Always both — see the units warning above |
| `max_fee_raw` | `0` on Standard |
| `is_fast` | |
| `source_chain_id`, `dest_chain_id` | |
| `burn_tx_hash`, `mint_tx_hash` | Present once each leg has a resolved hash |
| `mint_attempts`, `failure_reason` | Present when non-zero / set |
| `minted_amount`, `minted_amount_raw` | **Only ever present on `COMPLETED`.** Both are `null` in the one case below. |
| `minted_amount_unknown`, `minted_amount_note` | `COMPLETED`, but the credited amount could not be read (Fast transfers only). The USDC **did** arrive — that part is confirmed on-chain — and only the exact figure is missing. Relay the note; it sends the user to `wallet-balance`. |
| `funds_mid_flight`, `recovery` | See below |
| `note` | One-line explanation of why the job did not advance this pass. Worth relaying. |
| `verdict_withheld` | The job cannot yet be judged either way (still inside the burn grace window). It is **not** a failure — resume later. |
| `privy_status` | Diagnostic: the wallet provider's status for the transaction being tracked |
| `lease_held` | Another process is already advancing this job; nothing was submitted |
| `next_step` | Present while the job is unfinished |
| `agent_guidance` | Present only while the job is unfinished; the state-accurate reporting contract described below |

Statuses run `INITIATED` → `BURN_SUBMITTED` → `ATTESTED` → `MINT_SUBMITTED` → `COMPLETED`, with `FAILED` as the other terminal state. **Only `COMPLETED` means the money arrived** — see `../SKILL.md` for the reporting rule.

`agent_guidance.current_stage` maps the stored status without inference:

| Job status | `current_stage` | Meaning |
|---|---|---|
| `INITIATED` | `BURN_CONFIRMATION_PENDING` | The burn transaction was sent to the wallet provider; its on-chain success/hash is not confirmed yet |
| `BURN_SUBMITTED` | `ATTESTATION_PENDING` | The burn is confirmed; Circle attestation is pending |
| `ATTESTED` | `SERVER_MINT_PENDING` | Attestation is available; the server mint is pending |
| `MINT_SUBMITTED` | `MINT_CONFIRMATION_PENDING` | The mint transaction was submitted; its confirmation is pending |

The object also carries `remaining_stages`,
`completion_mode: SERVER_RELAY_WITH_CLI_FALLBACK`, the read-only
`status_command`, `do_not_start_new_transfer`, and
`user_action_required: CHECK_STATUS_LATER`.
Cover every field when reporting to the user. Translate the identifiers rather
than quoting them mechanically, but do not claim a later stage than
`current_stage`.

After starting or resuming a non-terminal bridge, report the decimal amount and symbol, name both source and destination chains, and distinguish burn submission, attestation waiting, and the server relay's future mint. Never call `INITIATED` or `BURN_SUBMITTED` complete. Tell the user to check the existing job instead of starting the transfer again, and never expose raw base units.

`COMPLETED` with `minted_amount_unknown: true` still means the USDC arrived. Preserve `minted_amount_note` and use `amb wallet-balance <wallet_address>` to verify the current balance; do not describe the null amount as a failed bridge.

### Funds mid-flight (`FAILED` with money in between)

A `FAILED` job whose burn landed but whose mint never did leaves USDC on neither chain. That response carries `funds_mid_flight: true` and a `recovery` text.

**Relay the `recovery` text to the user verbatim.** The job exists only in this machine's local SQLite — no server can reconstruct it — so the user's own `bridge-usdc-status` output is the only recovery input support will ever get. Nothing is lost; the transfer can be finished manually from that output.

### Error codes

| Code | Meaning / action |
|---|---|
| `BRIDGE_NOT_CONFIGURED` | This build has no bridge. Nothing the user can fix. |
| `BRIDGE_AMOUNT_INVALID` | Not a decimal USDC amount (digits, at most 6 decimal places, no sign or exponent). |
| `BRIDGE_AMOUNT_BELOW_MIN` | Below the build-configured minimum bridge amount. Nothing was submitted. |
| `BRIDGE_INSUFFICIENT_USDC` | Source-chain USDC is short of `amount + maxFee`. Nothing was submitted; the message breaks out both parts. |
| `BRIDGE_FEE_NOT_AUTHORIZED` | A Fast transfer's fee is not covered by a standing approval for this wallet. **Nothing was submitted.** Approve a ceiling with `bridge-fast-grant`, or drop `--fast` (Standard costs nothing). The check runs against the fee computed at start, so a fee that rose since you quoted is refused rather than spent. |
| `BRIDGE_JOB_IN_FLIGHT` | A bridge is already running for this wallet. Resume it instead (`amb bridge-usdc <wallet>`). |
| `BRIDGE_NO_ACTIVE_JOB` | Resume was called but nothing is unfinished. Pass an amount to start one. |
| `BRIDGE_JOB_NOT_FOUND` | That `job_id` does not belong to that wallet. |
| `BRIDGE_SPONSOR_NOT_ALLOWED` | **Operational, not the user's fault.** The gas sponsor rejected the batch (403) because the CCTP rules are not deployed to the sponsor allowlist for this environment. **No USDC was burned.** Retrying will not help — report it. |
| `BRIDGE_CLOCK_SKEW` | This machine's clock has drifted more than 5 minutes from the server's, so the request was rejected as expired. **Retrying fails identically** — sync the system clock (enable NTP), then re-run. It was deliberately not retried. |
| `BRIDGE_NOT_ATTESTED` | Internal: a mint was attempted with no message/attestation stored yet. Resume. |
| `BRIDGE_NO_TRANSACTION_ID` | The mint was submitted but the server returned no transaction id, so its hash cannot be resolved. Resume and report if it repeats. |

Exit codes follow the `deposit` convention: `0` for `COMPLETED` or a normal unfinished return, `1` for pre-flight/config/network errors, `2` for a `FAILED` job.

## Collateral Management

### supported_tokens - List supported deposit tokens

```bash
amb deposit-tokens [network]
```

Lists every token that can be deposited as collateral on a network, with the global MVL minimum required balance. **This is the authoritative answer to "what can I deposit?" and the way to obtain a token address for `deposit-add`.**

- If `network` is specified, shows tokens for that network only.
- If omitted, shows all configured deposit networks.

Output shape (`amb deposit-tokens ETHEREUM`):
```json
{
  "networks": [
    {
      "network": "ETHEREUM",
      "tokens": [
        { "token": "0xA849...", "symbol": "MVL",  "name": "Mass Vehicle Ledger Token", "decimals": 18 },
        { "token": "0xA0b8...", "symbol": "USDC", "name": "USD Coin",                  "decimals": 6  }
      ],
      "minRequiredMvl": "40000000000000000000000"
    }
  ],
  "errors": []
}
```
- `tokens`: MVL comes first — it is credited 1:1, so `minRequiredMvl` is the amount to send. The rest are convertible tokens, credited at the backend's quoted rate. `symbol`/`name`/`decimals` **may be `null`** when the metadata lookup failed; `token` (the address) is always present, and that is the field `deposit-add` needs.
- `minRequiredMvl`: raw wei units of MVL the agent ledger must hold for the deposit to be considered active. **May be `null`** if that one read failed; the token list is still valid.
- `errors`: failures, as `{ network, error }`. A network can appear in **both** `networks` and `errors` — a partial failure (one convertible token's metadata, or the threshold) does not remove the rest. Read `errors` before treating a short list as complete.

If MVL itself cannot be resolved the whole network goes to `errors` instead, because a list that silently omits MVL would say "USDC only" about a chain that accepts MVL.

Do not infer the list from anywhere else. The two kinds of token live in different places on-chain (MVL in the ledger's `mvlToken()`, the convertible tokens in the router's whitelist), and reading only one of them is how "MVL is not accepted" gets reported to users who could have deposited it.

### deposit_check - Check collateral balance

```bash
amb deposit-status <wallet_address>
```

Returns per-network collateral status. v2 model: a single MVL ledger balance (`deposited`) is compared against a global `minRequired` threshold; there is no per-token active flag.

The top-level `anyActive` is `true` if **any network** has `isActive: true` (OR condition).

Output shape (`amb deposit-status <wallet>`):
```json
{
  "anyActive": false,
  "networks": [
    {
      "network": "BASE_SEPOLIA",
      "isActive": false,
      "deposited": "0",
      "minRequired": "10000000000000000000",
      "nextWithdrawAt": 0,
      "mvlReserve": "5000000000000000000000",
      "mvlGap": "10000000000000000000",
      "requiredToActivate": [
        {
          "tokenAddress": "0xabc...",
          "symbol": "USDC",
          "tokenWei": "4000000",
          "ratePreview": "1000",
          "display": "~4.00 USDC to activate"
        }
      ],
      "requiredToActivateReason": null
    }
  ],
  "errors": []
}
```
- `deposited`: raw wei of MVL currently in the agent's ledger slot.
- `minRequired`: raw wei threshold (same as `minRequiredMvl` from `deposit-tokens`).
- `nextWithdrawAt`: Unix timestamp (seconds) after which withdrawal is permitted; `0` means no cooldown / no prior withdraw.
- `mvlReserve`: raw wei of MVL held by the router as the global reserve backing convertible-token deposits (Path B). Diagnostic — most agents can ignore this; surfaced for ops debugging when a convertible-token deposit fails with insufficient reserve.
- `errors`: per-network RPC failures.

Each network entry also includes activation guidance:

- `mvlGap`: MVL wei (string) still needed to reach `minRequired`; `"0"` when the threshold is already met.
- `requiredToActivate`: array of `{ tokenAddress, symbol, tokenWei, display, ratePreview? }` — each entry is one way to reach the minimum. `null` only when the gap is `0` (the agent is already active).
  - The **MVL entry always comes first and is always present** while a gap exists. MVL is credited 1:1, so `tokenWei` is exactly the gap, `display` carries no `~` (e.g. `"40000 MVL to activate"`), and `ratePreview` is **absent** — there is no conversion to preview.
  - Convertible entries (USDC, …) are best-effort: they need a SIWE JWT and the server rate endpoint. `display` is an estimate (`"~4.00 USDC to activate"`) and `ratePreview` is a display-only rate string.
- `requiredToActivateReason`: `null` | `"NO_JWT"` (no wallet login — follow `requiredToActivateHint`: typed login for MetaMask, legacy SIWE for Privy) | `"RATE_UNAVAILABLE"` (rate service error / no convertible tokens). **It describes the convertible-token half only.** A non-empty array alongside a non-null reason is normal and means "MVL is available; the converted options could not be computed" — do not read it as a total failure.
- `requiredToActivateHint`: present only for `NO_JWT`; a one-line next-step string. Absent (or `null`) in all other cases.

So a user who has not logged in yet still gets an actionable answer:

```json
"requiredToActivate": [
  { "tokenAddress": "0xA849…", "symbol": "MVL", "tokenWei": "40000000000000000000000",
    "display": "40000 MVL to activate" }
],
"requiredToActivateReason": "NO_JWT"
```

The MVL guidance itself is available without logging in. A Privy MVL deposit also needs no JWT because it goes straight to the ledger; a MetaMask MVL deposit uses the signature relay and therefore needs a cached JWT.

Chain reads always render regardless — a rate-service failure never blocks the rest of `deposit-status`.

The collateral selection policy is identical for Built-in Privy and MetaMask. Present the
returned `requiredToActivate` MVL/USDC options and ask the user which asset to use. Run
`amb wallet-balance <wallet_address>` and match its network/token row; compare its decimal
`amount` with the selected option's human-readable `display` amount. If the balance is short,
report the shortfall and stop rather than choosing or funding another asset. Otherwise, state
the network, asset, and amount, get confirmation, run `amb deposit-add` with the selected
option's exact `tokenAddress` and raw `tokenWei`, and finish by running `amb deposit-status`
again. Wallet type changes only execution: Privy MVL is sponsored/direct; MetaMask MVL uses
`ROUTER_SIG` and may need a one-time gas-paid allowance approval.

### deposit_token - Deposit token collateral

```bash
amb deposit-add <wallet_address> <network> <token_address> <amount> [--no-wait]
```

- `wallet_address`: Wallet address (0x...)
- `network`: Deposit network name (e.g. `BASE_SEPOLIA`, `ETHEREUM`)
- `token_address`: Token contract address. **Run `amb deposit-tokens <network>` to get it** — that command lists every depositable token for the network, MVL included, with its address. The command first identifies MVL vs. a convertible token, then chooses the signing path for the registered wallet.
- `amount`: Raw units in the token's own decimals (MVL has 18 decimals → 1 MVL = "1000000000000000000"; USDC has 6 decimals → 1 USDC = "1000000").

**Path A1 — MVL with a Privy wallet (direct deposit):**

When `token_address` matches the MVL token for the specified network, the command executes a `wallet_sendCalls` batch containing:
1. MVL `approve` (agent router as spender)
2. Router `depositMVL` (move MVL from agent wallet to agent ledger)

Both calls are executed in a single batch with Privy sponsorship (`sponsor: true`). The agent's native token balance remains 0 (gas is covered).

Success response:
```json
{
  "path": "mvl-direct",
  "token": "0x1234...",
  "agent": "0x5678...",
  "amount": "1000000000000000000",
  "batch_tx": {
    "kind": "transaction_id",
    "transaction_id": "tx_abc123",
    "caip2": "eip155:84532"
  }
}
```

- `batch_tx.transaction_id`: Blockchain transaction identifier (not a user-operation hash).
- To confirm the deposit landed, run `amb deposit-status <wallet_address>` (reads on-chain ledger state).

**Path A2 — MVL with a MetaMask wallet (`ROUTER_SIG` relay):**

MetaMask cannot use Privy's sponsored atomic batch. The command instead fetches the server's
`ROUTER_SIG` capability and signs the router's exact EIP-712 envelope (`DepositRouter`, version
`1`, `DepositMVL(address agent,uint256 amount,uint256 nonce,uint256 deadline)`). The raw 65-byte
signature is submitted to the relay; the client never splits it into `v`/`r`/`s`.

MVL has no permit/EIP-3009 support, so the router still needs ERC-20 allowance. If allowance is
short, the command first asks MetaMask to approve `uint256.max` and waits until that allowance is
visible on-chain before signing/submitting the deposit. This approval uses the wallet's native
gas. It is intentionally max allowance so subsequent deposits can remain gasless; if sufficient
allowance already exists, no approval transaction is sent.

Prerequisites:

1. `mm` is authenticated and its active address is the registered MetaMask wallet.
2. A cached JWT exists. Obtain it with `amb siwe-request-typed`, sign its file with
   `amb wallet-sign <wallet> eth_signTypedData_v4 <typed_file>`, then run
   `amb typed-submit <typed_file> <signature>`. If signing returns `approval_pending`, ask the
   user to approve it and rerun that exact `wallet-sign` command; do not switch to `personal_sign`.
3. The wallet holds enough MVL, and enough native gas for the first approval if allowance is low.
4. The configured network and gateway advertise a matching `ROUTER_SIG` capability.

The default command polls to a terminal relay state. A first-deposit response retains the approval
hash so both transactions can be audited:

```json
{
  "path": "mvl-sig-relay",
  "token": "0x0283...",
  "agent": "0x5678...",
  "amount": "1000000000000000000",
  "approve_tx": "0xapprove...",
  "request_id": "req_abc123",
  "status": "CONFIRMED",
  "mvl_amount": "1000000000000000000",
  "tx_hash": "0xdeposit..."
}
```

`approve_tx` is absent when existing allowance was reused. With `--no-wait`, the command returns
the PENDING request immediately and it can be resumed with `deposit-relay-status`.

The CLI keeps the exact signed request in local state until a terminal result has been printed.
If the relay POST response is lost, re-running the same `deposit-add` command re-submits that exact
signature so the server returns its idempotent original request; it does not create a new nonce.
While that request is unresolved, another MVL amount for the same wallet/network/token fails with
`MVL_DEPOSIT_IN_FLIGHT`. A concurrent invocation that arrives while MetaMask is still approving or
signing fails with `MVL_DEPOSIT_PREPARING` before opening a second wallet prompt. Follow the held
MetaMask request's approval instructions rather than retrying it in parallel.

**Path B — Convertible token deposit (e.g. USDC), gasless relay:**

When `token_address` is **not** the MVL token, the command routes the deposit through the agent-deposit relay: it fetches a backend-signed PriceQuote (token→MVL conversion), wraps an EIP-3009 `receiveWithAuthorization` for the agent's Kernel smart account, and submits it via the relayer. No native gas is needed — the relayer pays. Requires a valid cached JWT.

> - **Credited as MVL** — the deposited token is converted to an MVL ledger credit at the backend's quoted rate. The blocking response includes `mvl_amount` (the quoted MVL credit, wei). A later `deposit-withdraw` returns MVL, not the token you deposited.

By default the command **blocks**, polling the relay until it reaches a terminal state, then emits:
```json
{
  "path": "relay",
  "request_id": "req_abc123",
  "status": "CONFIRMED",
  "mvl_amount": "959000000000000000000",
  "tx_hash": "0x..."
}
```

- `mvl_amount`: quoted MVL credit (wei) that will be credited on CONFIRMED.

With `--no-wait` it returns immediately with the PENDING relay result (`{ "path": "relay", "request_id": "req_abc123", "status": "PENDING", "mvl_amount": "959000000000000000000" }`); poll it yourself with `amb deposit-relay-status <wallet_address> <request_id>` until `CONFIRMED` or `FAILED`.

When the relay cannot be used, the command fails with one of **two** codes. They look similar and are not interchangeable — the recovery is opposite, so read the code before advising anything:

| Code | What happened | Recovery |
|---|---|---|
| `RELAY_UNAVAILABLE` | The gateway could not be reached (down, non-2xx, unparseable). **Transient.** | Check the cached JWT and the gateway, then **retry**. |
| `TOKEN_NOT_DEPOSITABLE` | The relay answered and has no capability for this token on this network — it cannot be used as collateral. **Permanent.** | **Retrying will not help.** Run `amb deposit-tokens <network>` and use a listed token. The error names the MVL address, which remains available through the registered wallet's MVL path. |

Reporting the second as a connectivity problem sends the user to re-authenticate and check the gateway, neither of which can fix a wrong token address.

Either way, confirm the deposit landed with `amb deposit-status <wallet_address>` (reads the on-chain MVL ledger).

### deposit_relay_status - Poll a gasless relay deposit

```bash
amb deposit-relay-status <wallet_address> <request_id>
```

- `request_id`: from a `deposit-add` response when `path` is `"relay"` or `"mvl-sig-relay"`.
- Prints `{ request_id, status, tx_hash?, error_code?, error_message? }`. Exits non-zero when `status` is `FAILED`. Poll every ~3s until `CONFIRMED` or `FAILED`.

### withdraw - Withdraw collateral

```bash
amb deposit-withdraw <wallet_address> <network>
```

- `network`: Deposit network name (e.g. `BASE_SEPOLIA`, `ETHEREUM`).

v2 withdraws the **full MVL ledger balance** in one call — there is no token arg. The router calls `withdraw()` (no args); the agent-deposit ledger then transfers all credited MVL back to the agent EOA. Built-in Privy uses sponsored gas. MetaMask submits the same call directly through `mm`, so the selected wallet must hold native gas on the withdrawal network.

If MetaMask returns `MM_APPROVAL_PENDING` or an indeterminate request, ask the user to complete the external approval and then have the Agent rerun the identical `amb deposit-withdraw` command. The CLI privately retains the exact polling ID and watches that request instead of submitting another transaction. It deletes the resume state only after success or a definite terminal rejection. Never expose or manually use the polling ID.

> - **Returns MVL** — withdrawal always returns the **MVL token**, regardless of which token you originally deposited (e.g. a USDC deposit is refunded as MVL).

**Cooldown.** The ledger enforces a per-agent withdraw cooldown. Before sending the tx, the CLI reads `nextWithdrawAt(agent)`; if it is in the future, the command fails immediately with:

```
error: WITHDRAW_COOLDOWN: next withdraw allowed at unix <ts> (~<N> min from now). v2 enforces a per-agent withdraw cooldown.
```

Run `amb deposit-status <wallet_address>` to see the current `nextWithdrawAt`.

**Success response:**
```json
{
  "path": "mvl-withdraw",
  "agent": "0x5678...",
  "withdraw_tx": {
    "kind": "tx_hash",
    "tx_hash": "0xabc...",
    "explorer_url": "https://sepolia.basescan.org/tx/0xabc..."
  }
}
```

- `withdraw_tx`: `WalletSendTxResult` — MetaMask returns `kind: 'tx_hash'`; Privy may return `kind: 'tx_hash'` or `kind: 'user_operation_hash'` while the userOp is in flight.

**Back-compat.** Previous releases required a 3rd `<token>` positional. v2 ignores any value passed there and prints a stderr deprecation warning. The form will be removed in a later release; new scripts should drop it now.
