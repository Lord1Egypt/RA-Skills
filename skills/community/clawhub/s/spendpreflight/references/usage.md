# Usage and existing payment tools

Requires Node20+ and pinned `spendpreflight@0.4.0`. With operator permission, install inside this skill folder:

```sh
npm install --ignore-scripts --omit=dev --legacy-peer-deps --no-audit --no-fund
node examples/offline.mjs
node examples/online.mjs
```

Both examples are offline demonstrations. The online example injects mocked HTTP, human approval and native MCP calls: zero real requests/payments. It tests dispatch, not live delivery or compatibility with a user's particular tool.

## CLI

Pipe JSON on stdin; do not interpolate inputs into shell commands. Fields: `tool`, `input`, optional `policy`, optional `operation_id` (letters/digits/underscore/hyphen, max100). Example:

```json
{"tool":"ofac_address_check","input":{"address":"0x1111111111111111111111111111111111111111"}}
```

`node scripts/run.mjs` returns an offline hold. `node scripts/run.mjs --online` actually posts the free check. OFAC also accepts `addresses` with 1–10 items. Lint input is `{"url":"https://example.com/public-endpoint"}`; its unpaid derived report is public by link for seven days. No private URL, key or customer data belongs in a request. Errors never trigger paid fallback, polling or retries.

`preflight_payment` input has the actual x402v2 `challenge` and `selected_requirement` from `accepts`. `check_payee` has public `address`, `domain` and/or `name`. Both use the JSON Spend Policy shown in the offline example. Target-merchant policy does not authorize the separate service fee; the existing payment tool keeps enforcing its own spend limits. SDK previews are not a durable wallet-wide budget.

The CLI has no `--yes`, key, payment-header, module-loader or credential option. Online paid CLI mode obtains an unsigned quote and emits a proposal, but **cannot execute native payment MCP tools by itself**. The OpenClaw agent can use that proposal with its existing tools according to SKILL.md, or a trusted host can use the executable bridge below. A proposal/pending request is not a completed check.

## Runtime: an actual paid dispatch path

`createClient` from `scripts/online.mjs` accepts explicit `mode:'online'`, a normal unsigned `fetch`, `approve(proposal)`, and `paymentTool.execute(request)`. These runtime callbacks never come from request JSON. With mode omitted, fetch and callbacks are never invoked.

`approve` must show a real human the proposal and return `{approved:true, request_id:proposal.request_id}` only after approval of the exact input, fee and service payee. IDs are fresh and expire after two minutes. Never unconditionally approve in production. The frozen proposal/input digest bind reviewed input.

The payment adapter receives `url`, `method:'POST'`, `body`, decimal-USDC `maxPayment`, `expectedPayment` (scheme/network/asset/payee/atomic amount), `approval_id` and `input_digest`. It must call the existing configured tool, retain its caps, enforce reviewed terms before signing, and return the actual HTTP `{status,body}`. Incompatible schemas or unenforceable caps mean hold. No signer or credential reads belong in an adapter. This interface is a host integration boundary, not a claim that all x402 tools share an API.

For an already connected Coinbase Wallet MCP with its documented two-step API:

```js
import { createClient, createWalletMcpPaymentTool } from './scripts/online.mjs';
const paymentTool = createWalletMcpPaymentTool({
  callTool: (name,args) => existingNativeMcp.callTool({name,arguments:args}),
  confirmWallet: review => humanUi.waitForWalletApproval(review),
  readResponse: result => existingNativeMcp.readHttpResponse(result),
});
const client = createClient({mode:'online',paymentTool,
  approve: proposal => humanUi.approveExactServiceFee(proposal)});
const result = await client.run(publicRequest);
```

These are trusted-host callbacks, not built-in globals or a new connection. `initiate_x402_request` gets `{url,method:'POST',body,maxPayment}`. The adapter presents the returned `{requestId,approvalUrl}` to the human; they must verify the actual payee, Base USDC amount and request in their existing wallet. Only then may `confirmWallet` return true and `complete_x402_request({requestId})` run once. `readResponse` maps the actual provider envelope to `{status,body}`; inspect its schema rather than assuming a layout. Missing/denied wallet approval returns hold with the pending request ID. Resolve that same request after the human approves; never blindly rerun `client.run` and create another payment.

Older Coinbase payments MCP and other tools may have a different API. Use their actual connected schema and existing user-set per-call/session caps. Do not assume a missing hook, bypass caps, install a new wallet or request keys. Missing compatible transport means hold. The Coinbase adapter has mock coverage, not a live-wallet test.

The helper never pays the target merchant. Keep operation IDs/unknown outcomes in a host journal across restarts; the helper's attempt set is only in-process. Requests go to fixed SpendPreflight URLs with redirects disabled, timeouts and bounded responses. No automatic retry, trial, paid fallback, payment-header handling or key storage is implemented.

References: [Coinbase Wallet MCP](https://docs.cdp.coinbase.com/ai-agents/coinbase-for-agents/wallet-mcp#make-x402-payments), [SDK0.4.0](https://www.npmjs.com/package/spendpreflight/v/0.4.0), [SpendPreflight](https://docs.spendpreflight.com/mcp/), [OpenClaw format](https://docs.openclaw.ai/clawhub/skill-format).
