---
name: redotpay-payment
description: "use when the user asks RedotPay to find, search, request, or look up services/data. Covers service discovery by ```bash
redotpay wallet services list --search \"<keywords>\"
```  and data retrieval across media generation, model APIs, data APIs, and agent-commerce lookups. Triggers on 'use redotpay to find/search/look up/request XXX'."

---

# RedotPay Payment

Service discovery and data retrieval via CLI. **Find, search, and request only — no purchase/buy flows.**

## Prerequisites & Readiness Check

**Before any user-facing workflow, verify the `redotpay` binary is callable.**

### Step 0 — Environment Verify

```bash
command -v redotpay && redotpay --version
```

| Result | Action |
|--------|--------|
| `command not found` / no output | CLI not installed → run **Installation Reference** below |
| Found but `redotpay wallet whoami` fails with ENOENT | CLI installed but not in Gateway PATH → run **Link to Gateway PATH** below |
| Found + version prints | Ready → skip to Core Workflow |


Then re-run the verify check above.

### Link to Gateway PATH

`~/.local/bin` is guaranteed to be in the OpenClaw Gateway launchd PATH. If `redotpay` is installed under `~/.redotpay/bin/` but not found, create the symlink:

```bash
ln -sf ~/.redotpay/bin/redotpay ~/.local/bin/redotpay
```

> **Why:** Gateway runs via launchd and does not source `.zshrc` / `.bashrc`. Non-standard PATH directories like `~/.redotpay/bin` must be linked into a standard location already in the Gateway PATH (`~/.local/bin`).

> **If Gateway still can't find `redotpay` after linking:** reload Gateway with `openclaw gateway restart`.

After linking, re-run `command -v redotpay && redotpay --version` to confirm.

---

## When to Trigger

Trigger when the user message combines RedotPay with a **discovery or query** action:

- `use redotpay to find/search/look up/request …`
- `request/find/search/look up … by/via redotpay`
- `用 redotpay 找/查/搜 …`

**Trigger examples:**

> "use redotpay to find running shoes under $150 with free shipping"
> "use redotpay to search flights SFO to Tokyo"
> "look up AAPL stock data by redotpay"
> "request weather data for NYC via redotpay"

---

## Task Buckets

RedotPay services are organized into these categories. Use them to guide keyword selection during service discovery:

### Generate Media
Image, video, music, audio, TTS, transcription.

### Model APIs
Chat completion, embeddings, inference.

### Data APIs
Search, extraction, on-chain data, travel/maps-style lookups (per catalog).

### Agent-Commerce
Buy/order/purchase flows exposed via MPP (lottery, domains, mail, etc.).

> **Note:** This skill handles discovery and data retrieval across all buckets. Agent-commerce **purchase** flows are excluded — only listing/searching/looking up commerce services is allowed.

---

## Core Workflow (Four Steps)

**Steps 1, 2, 3 do not require login.** Login is only needed at Step 4 before making a paid request.

### Step 1 — Search for Services

```bash
redotpay wallet services list --search "<keywords>"
```

Extract 1–3 core keywords from the user's request. Match against the task buckets above:

| User Request | Bucket | Search Terms |
|-------------|--------|-------------|
| Find running shoes under $150 | Data APIs | `--search "shoes product search"` |
| Search flights SFO→JFK | Data APIs | `--search "flight travel"` |
| Look up AAPL stock | Data APIs | `--search "stock market finance"` |
| Generate an image of a cat | Generate Media | `--search "image generation"` |
| Transcribe this audio file | Generate Media | `--search "transcription audio"` |
| Chat with GPT about history | Model APIs | `--search "chat completion llm"` |

If results are empty, try broader keywords. Output is JSON — focus on `id`, `name`, `description`, `serviceUrl`.

### Step 2 — Inspect the Service

```bash
redotpay wallet services <service_id>
```

Get endpoint list, parameter schema, and pricing. **Always inspect before calling.**

### Step 3 — Quote Cost and Get Confirmation

**After inspecting the service and mapping user constraints to parameters, before any request:**

1. Tell the user:
   - Which service and endpoint will be called
   - Exact cost in **USD** (convert from the service's native currency; stablecoins like USDC/USDT = 1:1 USD; for other tokens, note both the raw amount and estimated USD value)
   - What the request will return
2. **Wait for explicit user confirmation.** Do not proceed without it.
3. If user says no or asks for alternatives, go back to Step A or B.

### Step 4 — Login then Call the Service

**Login is only required at this step.**

First, check login status:

```bash
redotpay wallet whoami
```

- Logged in → proceed to call the service
- Not logged in → run login flow (see Login Flow below), then proceed

Then call the service:

```bash
redotpay request [flags] <endpoint_url>
```

Only execute after Step 3 confirmation and login check.

---

## Command Reference

```text
redotpay wallet services list [--search <q>]  # Search services
redotpay wallet services <id>                  # Inspect service details
redotpay request [curl-flags] <url>            # Send request
redotpay wallet whoami                         # Check login status
redotpay wallet login                          # Log in
redotpay wallet logout                         # Log out
redotpay --help                                # Help
redotpay request --help                        # Request help
redotpay guide                                 # Usage guide
```

---

## Payment Safety Rules

### User Confirmation

1. Login (`wallet login`) does not require confirmation for a specific charge.
2. Any paid `redotpay request` must:
   - State the cost in **USD**, the purpose, and the original currency/amount
   - Obtain **explicit user confirmation** before executing

### Spend Cap

Set a cap via `--max-spend` or `REDOTPAY_CLI_MAX_SPEND` for any chargeable request. If the user refuses a cap, do not proceed.

### Preflight

Login is only required at Step 4. Do **not** run `whoami` or `login` during Steps 1, 2, or 3.

---

## Login Flow

Only triggered at Step 4 when `whoami` returns "not logged in".

```bash
redotpay wallet login
```

1. Parse stdout JSON, extract `login_qr_png_path` and `user_code`
2. Read and display the QR image as an attachment: `read <login_qr_png_path>`
3. Tell the user: **Open the RedotPay app, scan the QR code above to authorize**
4. Wait for user → `whoami` to confirm → continue

---

## Troubleshooting

### Skill not appearing in available skills list

**Root cause:** `redotpay` binary not found in Gateway PATH.

1. Run `command -v redotpay` in terminal — if found, note the path (typically `~/.redotpay/bin/redotpay`)
2. Check if that directory is in the Gateway launchd PATH: inspect `~/Library/LaunchAgents/ai.openclaw.gateway.plist` → `EnvironmentVariables` → `PATH`
3. If missing, create symlink: `ln -sf ~/.redotpay/bin/redotpay ~/.local/bin/redotpay`
4. Restart Gateway: `openclaw gateway restart`
5. `command -v redotpay` should now succeed in the Gateway context

### `redotpay request` returns 402 / payment error

1. Ensure wallet is logged in: `redotpay wallet whoami`

### Service returns empty results

1. Broaden keywords in `redotpay wallet services list --search`
2. Check the service catalog for available categories
3. Some services require specific parameter formats — always inspect with `redotpay wallet services <id>` before calling

---

---

## After setup

Provide:

- RedotPay readiness **only from** `redotpay wallet whoami`.
- Whether the task is MPP discovery, direct redotpay request, or 402 retry.
- If login is required, follow **Login Flow** only (QR + **RedotPay app** scan reminder ; no token dumps).

---

## Use services and requests

```bash
redotpay wallet services list
redotpay wallet services list --search <query>
redotpay wallet services <service_id>
redotpay request [curl-like flags] <URL>
```

- Use `redotpay wallet services` for mpp.dev-style public registry discovery (`id`, `name`, `serviceUrl`, etc.).
- Use `redotpay request` as the curl-like HTTP entrypoint, including paid endpoints that may return 402.

---

## Preflight (mandatory for `redotpay request`)

Before **any** `redotpay request`, run **`redotpay wallet whoami`** first.

If **not logged in** or session invalid: **do not** call the URL yet or blindly retry. **Pause**, run **Login Flow** end-to-end (including **RedotPay app** QR scan instructions), wait until the user finishes authorization, then `whoami` until it is good; **then** run or retry `redotpay request`.

`redotpay wallet services …` may work without a session in some setups; paid or session-gated calls still require the rule above.

### Request examples

```bash
redotpay request https://example.com/resource
redotpay request -X POST https://example.com/api -H 'Content-Type: application/json' --json '{"a":1}'
```

---

## HTTP 402 behavior (`redotpay request`)

Many paid flows return `402 Payment Required`. `redotpay request` supports behaviors described in CLI help, including:

### If a 402 lists Tempo as a payment method

Do **not** assume you must switch to `tempo` or `mppx`.

In this model, `redotpay request` can still complete payment when Tempo appears in offered methods, using RedotPay OAuth session (`redotpay wallet login`) plus normal redotpay request semantics.

For edge cases, consult `redotpay guide` and CLI help before guessing.

---

## Agent UX before charging

1. State amount, currency, and purpose when known.
2. **Consent vs login:** you may run **`redotpay wallet login`** as soon as `whoami` shows no session (identity only). That is **not** consent for a **specific charge** — get explicit agreement on amount/currency/purpose before a **paid** `redotpay request` (or before approving spend on a retry after login).
3. **Preflight:** `whoami` before every `redotpay request`; if no session → **Login Flow** (QR + **tell the user to open the RedotPay app and scan to authorize**) → then request.
4. Never paste OAuth tokens, raw wallet payloads, or full credential files into chat.

---

## Safety

- Never request, print, or store OAuth tokens, API keys, or signing material in chat.
- Treat local RedotPay wallet config as sensitive; do not dump credential stores or full config.
- Use verbose mode (`-v`) sparingly because stderr may expose URL/payment metadata.

---


## Notes

- Never expose OAuth tokens, keys, or wallet config in chat
- Use `-v` sparingly (stderr may leak payment metadata)
- **Login QR:** use `read` tool on the PNG path, not `![...](file://...)` markdown (blocked by browser security)

---

## Installation Reference

Manual first-time setup (normally handled automatically by the Prerequisites check above).

```bash
curl -fsSL "https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.1/install.sh" -o redotpay-install.sh
shasum -a 256 -c SHA256SUMS --ignore-missing
bash redotpay-install.sh
redotpay --version
```