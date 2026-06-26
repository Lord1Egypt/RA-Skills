---
name: redotpay-payment
description: "Trigger when the user asks RedotPay to find, search, request, or look up services/data. Covers service discovery by ```bash
redotpay wallet services list --search "<keywords>"
```  and data retrieval across media generation, model APIs, data APIs, and agent-commerce lookups. Triggers on 'use redotpay to find/search/look up/request XXX'."
metadata: {"openclaw":{"requires":{"bins":["redotpay"]}}}
---

# RedotPay Payment

Service discovery and data retrieval via CLI. **Find, search, and request only — no purchase/buy flows.**

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

**Steps A, B, C do not require login.** Login is only needed at Step D before making a paid request.

### Step A — Search for Services

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

### Step B — Inspect the Service

```bash
redotpay wallet services <service_id>
```

Get endpoint list, parameter schema, and pricing. **Always inspect before calling.**

### Step C — Quote Cost and Get Confirmation

**After inspecting the service and mapping user constraints to parameters, before any request:**

1. Tell the user:
   - Which service and endpoint will be called
   - Exact cost (amount + currency)
   - What the request will return
2. **Wait for explicit user confirmation.** Do not proceed without it.
3. If user says no or asks for alternatives, go back to Step A or B.

### Step D — Login then Call the Service

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

Only execute after Step C confirmation and login check.

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
   - State amount, currency, and purpose
   - Obtain **explicit user confirmation** before executing

### Spend Cap

Set a cap via `--max-spend` or `REDOTPAY_CLI_MAX_SPEND` for any chargeable request. If the user refuses a cap, do not proceed.

### Preflight

Login is only required at Step D. Do **not** run `whoami` or `login` during Steps A, B, or C.

---

## Login Flow

Only triggered at Step D when `whoami` returns "not logged in".

```bash
redotpay wallet login
```

1. Parse stdout JSON, extract `login_qr_png_path` and `user_code`
2. Read and display the QR image as an attachment: `read <login_qr_png_path>`
3. Tell the user: **Open the RedotPay app, scan the QR code above to authorize**
4. Wait for user → `whoami` to confirm → continue

---

## Notes

- Never expose OAuth tokens, keys, or wallet config in chat
- Use `-v` sparingly (stderr may leak payment metadata)
- **Login QR:** use `read` tool on the PNG path, not `![...](file://...)` markdown (blocked by browser security)

---

## Installation Reference

For first-time setup only.

```bash
curl -fsSL "https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.0/install.sh" -o redotpay-install.sh
shasum -a 256 -c SHA256SUMS --ignore-missing
bash redotpay-install.sh
redotpay --version
```
