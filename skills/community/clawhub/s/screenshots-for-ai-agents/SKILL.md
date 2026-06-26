---
name: screenshot-x402-mcp
description: >-
  Browser screenshots and vision over MCP Streamable HTTP with x402 USDC
  micropayments at this deployment. Paid tools require an x402-aware MCP client
  and a funded wallet (or platform-managed signer); URLs and page-derived data
  are processed off-host here. Triggers: take_screenshot, analyze_screenshot,
  discovery.json, pay-per-call capture, Streamable HTTP MCP, 402 payment.
homepage: https://screenshotx402.com
metadata:
  version: 2
  transport: streamable-http
  payment: x402
---

# screenshot-x402 — MCP screenshots + x402

Remote **Model Context Protocol** server (**Streamable HTTP** only). All tools are invoked through MCP — there is no separate REST “screenshot URL” for paid capture.

**Base URL:** `https://screenshotx402.com`  
**MCP endpoint:** `https://screenshotx402.com/mcp`

## Before you install or use

1. Read **`https://screenshotx402.com/discovery.json`** for **list prices**, **x402 network**, and **`mcp.url`** — avoid surprise charges.
2. Confirm your **agent host** can run an **x402-aware MCP client** and **sign USDC** payment authorizations on that network.
3. **Trust this deployment** (`https://screenshotx402.com`) before placing **wallet / signing secrets** in environment or vaults.
4. Call **`health`** (free) before paid tools.

## Credentials and signing (paid tools only)

**Free:** `health` and discovery HTTP need **no** wallet.

**Paid** (`take_screenshot`, `analyze_screenshot`): the client must **sign** x402 **USDC** authorizations and **retry** with payment proof headers (e.g. `PAYMENT-SIGNATURE` / `X-PAYMENT`). Use a stack such as Cloudflare **`agents/x402`** **`withX402Client`** with a **viem** account. **Private keys** belong in **your** host env (examples in project docs: **`AGENT_PRIVATE_KEY`**, **`X402_PRIVATE_KEY`** in sample clients) — **never** in prompts. The signer needs **USDC** on the advertised network.

If your platform cannot attach payment proofs, use only free discovery + **`health`**, or another capture method.

## Privacy and off-host data

**URLs** you submit are sent to **this deployment** (`https://screenshotx402.com`). The service **fetches and renders** pages on operator infrastructure; **screenshots** and, for **`analyze_screenshot`**, your **prompt** and vision output, are processed **off your machine**.

**Do not** use for non-public or sensitive URLs (internal hosts, auth-gated content you cannot leak, secrets in query strings). Use local or self-controlled tooling for private systems.

## Discovery (free HTTP)

| Resource          | URL                                         | Purpose                                          |
| ----------------- | ------------------------------------------- | ------------------------------------------------ |
| This skill        | `https://screenshotx402.com/skill.md`       | Human + agent onboarding (this file)             |
| Machine discovery | `https://screenshotx402.com/discovery.json` | `mcp.url`, `x402Network`, tool list, list prices |
| API reference     | `https://screenshotx402.com/docs`           | Full parameter tables and return shapes          |
| Landing           | `https://screenshotx402.com/`               | Tools overview and examples                      |

Always read **`https://screenshotx402.com/discovery.json`** for current USD list prices — do not hard-code amounts.

## Tools overview

| Tool                 | Cost        | Purpose                                          |
| -------------------- | ----------- | ------------------------------------------------ |
| `health`             | Free        | Smoke test MCP + advertised x402 network         |
| `take_screenshot`    | x402 / USDC | Browser PNG or JPEG of a public `https` URL      |
| `analyze_screenshot` | x402 / USDC | JPEG capture + vision text answer to your prompt |

## x402 payment flow (MCP)

This service uses **MCP tool calls** instead of raw `GET /api/...`, but the idea matches HTTP x402:

1. **Connect** a Streamable HTTP MCP session to `https://screenshotx402.com/mcp`.
2. **Call** a paid tool (`take_screenshot` / `analyze_screenshot`) with normal `arguments`.
3. **First response** encodes **payment required**: tool result includes x402 metadata (version, `accepts` with price, network, pay-to, asset, facilitator expectations). No image payload yet.
4. **Complete** the USDC payment on the chain advertised in that payload (this deployment’s network in discovery is **`base`** — confirm in `discovery.json` / `health`).
5. **Retry** the **same** `callTool` with the payment proof attached the way your MCP client expects (e.g. `PAYMENT-SIGNATURE` / `X-PAYMENT` on the MCP HTTP session, per your stack).
6. **Server** verifies via the facilitator, then returns the real tool result (image and optional text).

**Automatic handling:** Use an **x402-aware MCP client** (for example Cloudflare **`agents/x402`** `withX402Client` around the MCP `Client`) so payment discovery, signing, and retries are handled like an x402 HTTP client would handle `402` + `X-Payment` — without you manually copying headers.

## 1. `health` (free)

**MCP:** `callTool` with name `health`, `arguments`: `{}`.

**Parameters:** none (empty object).

**Successful result (shape):**

```json
{
  "content": [
    {
      "type": "text",
      "text": "{ \"ok\": true, \"name\": \"screenshot-x402\", \"x402Network\": \"base\" }"
    }
  ]
}
```

`content[0].text` is a **JSON string** — parse it for `ok`, `name`, `x402Network`.

## 2. `take_screenshot` (paid — x402)

**MCP:** `callTool` → `take_screenshot`.

**Parameters:**

| Param             | Type         | Required | Default         | Description                               |
| ----------------- | ------------ | -------- | --------------- | ----------------------------------------- | ------ | --------------- |
| url               | string (URL) | yes      | —               | Absolute `https://` page to capture       |
| width             | number       | no       | 1920            | Viewport width (100–3840)                 |
| height            | number       | no       | 1080            | Viewport height (100–2160)                |
| fullPage          | boolean      | no       | false           | Capture full scrollable page              |
| delay             | number       | no       | 0               | Extra wait after load (ms, max 30000)     |
| cacheTtl          | number       | no       | 86400           | R2 cache TTL seconds; 0 skips cache reads |
| format            | string       | no       | `png`           | `png` or `jpeg`                           |
| colorScheme       | string       | no       | `no-preference` | `light`                                   | `dark` | `no-preference` |
| deviceScaleFactor | number       | no       | 1               | Pixel ratio 1–3 (sharpness)               |
| hideSelectors     | string[]     | no       | `[]`            | Up to 40 CSS selectors to hide            |

**Successful result (shape):**

```json
{
  "content": [
    {
      "type": "image",
      "data": "<base64 PNG or JPEG>",
      "mimeType": "image/png | image/jpeg"
    }
  ],
  "_meta": {
    "cached": true,
    "renderTimeMs": 1234
  }
}
```

`_meta.cached` and `_meta.renderTimeMs` may be omitted depending on path.

## 3. `analyze_screenshot` (paid — x402)

**MCP:** `callTool` → `analyze_screenshot`.

**Parameters:**

| Param             | Type         | Required | Default         | Description                               |
| ----------------- | ------------ | -------- | --------------- | ----------------------------------------- |
| url               | string (URL) | yes      | —               | Page to capture                           |
| prompt            | string       | yes      | —               | Question/instruction for the vision model |
| width             | number       | no       | 1920            | Viewport width                            |
| height            | number       | no       | 1080            | Viewport height                           |
| fullPage          | boolean      | no       | false           | Full page capture                         |
| colorScheme       | string       | no       | `no-preference` | Same as `take_screenshot`                 |
| deviceScaleFactor | number       | no       | 1               | Same as `take_screenshot`                 |
| hideSelectors     | string[]     | no       | `[]`            | Same as `take_screenshot`                 |

**Successful result (shape):**

```json
{
  "content": [
    {
      "type": "image",
      "data": "<base64 JPEG>",
      "mimeType": "image/jpeg"
    },
    {
      "type": "text",
      "text": "<vision model answer>"
    }
  ],
  "_meta": {
    "renderTimeMs": 1234
  }
}
```

## Decision guide

| Goal                         | Tool                 | Cost                 |
| ---------------------------- | -------------------- | -------------------- |
| Verify MCP + network         | `health`             | Free                 |
| Still image capture          | `take_screenshot`    | Paid (see discovery) |
| Capture + describe / extract | `analyze_screenshot` | Paid (see discovery) |

## Constraints

- Targets must be **`https://`** URLs (see `/docs`).
- **Vision** output for `analyze_screenshot` depends on the **operator’s** server configuration (not something callers configure through MCP).

## More links

- [x402](https://www.x402.org/) · [MCP](https://modelcontextprotocol.io/)
