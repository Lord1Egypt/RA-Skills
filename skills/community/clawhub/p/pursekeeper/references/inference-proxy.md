# inference-proxy.js: the wallet is the budget

A localhost OpenAI-compatible proxy that pays for an agent's model calls in Nano, per call, from the
agent's own wallet, inside a cumulative cap the operator set before starting it. First version
2026-10-10 (initiative #12 at https://pursekeeper.dev; the source-level and install-level reviews
named there start at this tag and are paid on delivery).

Who it is for: an operator who already holds Nano, or buys it at an exchange or at Nanswap, and runs a
self-hosted agent runtime (OpenClaw, Pi, opencode, Codex CLI, Claude Code, goose, crush, anything that takes an
OpenAI-compatible base URL). The agent's model calls go to NanoGPT's accountless door
(https://nano-gpt.com/api/x402, hundreds of models, quoted per request, no account) and are paid from a
wallet the operator funded. Hosted runtimes (ChatGPT projects, hosted Claude, anything with no
base-URL setting and nowhere persistent to keep a key) cannot use this; Ops Control HQ's answer of
2026-10-08 is why that sentence is here.

## Setup, five minutes

```bash
cd <this skill's folder>/scripts && npm install          # nanocurrency, the only dependency
export NANO_SEED=$(openssl rand -hex 32)                  # or the seed of the wallet you funded; 600-mode file, never a log
node no-node.js address                                   # fund this address; ~0.01 XNO covers hundreds of small-model calls
node no-node.js receive                                   # pocket the funding send (opens the account)
export PROXY_KEY=$(openssl rand -hex 16)                  # the runtime presents this as its API key; nothing without it is paid
NANO_CAP=0.1 NANO_MAX_PER_CALL=0.01 UPSTREAM=https://nano-gpt.com/api/x402 node inference-proxy.js
```

Then point the runtime at `http://127.0.0.1:3402/v1` with `PROXY_KEY` as its API key
(`Authorization: Bearer <key>` or `x-api-key: <key>`; a `/v1/*` request without it is refused 401
with nothing forwarded or signed; until 0.3.0 any key was accepted). The proxy drops the
runtime's credential headers (`authorization`, `proxy-authorization`, `x-api-key`, `api-key`,
`x-auth-token`, `x-goog-api-key`, `cookie`) before the door sees them, on the paid path and on a
plain relay alike; every other request header is forwarded as is. Until 0.2.3 only `authorization`
and `proxy-authorization` were dropped, so a runtime sending its key as `x-api-key` forwarded it. `GET http://127.0.0.1:3402/_nano/state` shows the cap, the spend, the
refunds pocketed, every payment's block hash and status, and the last refusals.

Environment: `NANO_SEED` (required), `NANO_INDEX` (0), `PROXY_KEY` (required, 16+ characters; the
runtime's API key for this proxy), `UPSTREAM` (required; the one door this
instance may pay), `NANO_CAP` (required; cumulative, XNO as decimal text, over the life of the state
file), `NANO_MAX_PER_CALL` (0.001), `NANO_ALLOW_PAYTO` (optional comma list; NanoGPT issues a fresh
deposit account per payment, so leave it unset there), `STATE_FILE`
(`~/.pursekeeper/inference-proxy-<port>.json`), `PORT` (3402; the proxy binds 127.0.0.1 only, and loopback is shared with every process and browser
tab on the machine, which is what `PROXY_KEY` and the checks below are for), `NANO_RPC` (a node, else
pursekeeper.dev's free endpoints), `WORK_URL` (an RPC-style `work_generate` endpoint, else
pursekeeper.dev's free `/v1/work` at 6 a minute, else the CPU), `RECEIVE` (1: pocket refunds before a paid call).

## What happens on each request

0. Before anything is read, counted or signed: the `Host` header must be a loopback name
   (`127.0.0.1`, `localhost`, `[::1]`, with or without a port; a web page that rebinds its DNS to
   127.0.0.1 arrives with its own host name and is refused 403 `host_not_loopback`), there must be
   no `Origin` header (a browser sets one on every cross-site request, including the no-preflight
   POSTs a page may send to 127.0.0.1; refused 403 `browser_origin`), and a `/v1/*` request must
   carry `PROXY_KEY` (a page cannot set `Authorization` or `x-api-key` without a CORS preflight,
   which the proxy never answers; refused 401 `proxy_key`). These three are what stands between
   the wallet and anything else on the machine that can open a TCP connection to loopback.
1. The request is forwarded to `UPSTREAM` + path, body unchanged, the credential headers listed above removed.
2. Not a 402: relayed as is (status, body, streaming included).
3. A 402: the quote is read in one of two dialects, then one decision runs under a lock, before
   anything is signed. Every path out is a refusal to the runtime with nothing signed, or a payment:
   - the quote's `payTo` is a valid account and `amount` a positive integer in raw;
   - NanoGPT dialect: `completeUrl` and `statusUrl` are on the `UPSTREAM` host, a `paymentId`
     exists and has not been paid before by this state file (a repeated id is a replay, refused
     `paymentid_replayed`), `expiresAt` is present and at least 5 s away (a quote without one is
     `malformed_quote`; until 0.2.1 a missing field skipped the check);
   - exact dialect: the quote's `resource` (top-level, a string or `{url}`, or on the accepted
     option) is on the `UPSTREAM` host when present; one for another origin is refused
     `resource_mismatch` before signing;
   - `payTo` is on `NANO_ALLOW_PAYTO` when that is set;
   - `amount` is at most `NANO_MAX_PER_CALL`;
   - spent so far plus `amount` is at most `NANO_CAP`;
   - the account is opened and holds the amount.
4. The spend is written to the state file **before** the block is signed, so a crash overcounts
   rather than undercounts. Then:
   - **NanoGPT dialect** (`payment.accepted[]` with scheme `nano`): the proxy signs and broadcasts a
     send to the per-payment deposit account, polls `statusUrl` until the door reports the payment
     (a few seconds), and POSTs the same body to `completeUrl` with `x-x402: nano` and the payment
     id. A broadcast the node rejects is refused `broadcast_failed`; a broadcast whose outcome cannot be
     read stays counted as `unknown`. Either way the signed block is settled as described under
     "what did not land" below.
   - **x402 exact dialect** (`PAYMENT-REQUIRED` header, x402 v2, scheme `exact`, network
     `nano:mainnet`: @x402nano/exact, feeless402, pursekeeper.dev and most of
     https://pursekeeper.dev/sellers): the signed block travels in `PAYMENT-SIGNATURE` and the
     seller broadcasts it; a "not yet confirmed" 402 is re-presented for up to a minute with the
     seller's `X-Nano-Represent` token, never re-signed. A refusal after signing is checked against
     the chain: broadcast but not served stays counted and is reported with the hash and the token
     (`broadcast_not_served`); not broadcast is `not_broadcast_refused` and settled as below. The
     signed payload is not kept: a refused call is a new quote and a new send, never a re-presentation.
   - **What did not land.** A signed send that is not on the chain can still land for as long as the
     account's frontier is the block's `previous`: a seller that refused still holds a valid signed
     block, and a node that took a broadcast whose reply was lost may process it later. So such a
     send stays counted until it either lands or a different block is confirmed at its height, and
     the proxy forces the second outcome itself: it publishes a change block at that height (same
     balance, same representative, nothing moves; the work computed for the send is good for it).
     Once that block is confirmed, which takes well under a second on the live network, the send
     can never land and its amount is released from the cap. Each payment entry shows `counted`
     (inside the cap right now), `final` (settled for good) and `invalidated_by` (the change block).
     If the change block cannot be published, because the node is down, the amount stays counted,
     counts against the cap, and is retried at the next call and at every start. Until 0.3.1 a
     refused send was uncounted at once, which left one per-call amount per frontier that a seller
     could broadcast later outside the cap (the path llmrt's Review B report of 2026-10-13 documented; the gap was noted in the ruling on it).
5. The reply carries `x-payer-paid` (XNO), `x-payer-hash` (the block) and, for NanoGPT,
   `x-payer-payment-id`, plus the door's own `x-x402-*` headers.

Refusals answer HTTP 402 with `{"error":{"type":"nano_payer_refused","code":...},"payer":{...}}` and
an `x-payer-refused` header: `cap_exceeded`, `over_per_call_limit`, `payto_not_allowed`,
`host_mismatch`, `resource_mismatch`, `quote_expired`, `malformed_quote`, `paymentid_replayed`,
`no_nano_option`, `insufficient_balance`, `account_not_opened`, `broadcast_failed`. The gate in step 0
answers 403 `host_not_loopback` or `browser_origin`, and 401 `proxy_key`, in the same shape. A door that cannot be reached, or a paid call the door did
not serve, answers 502 with the hash and payment id so the call can be completed by hand within the
quote's life (NanoGPT: 15 minutes, same body, same payment id).

Concurrency: payments are serialised; parallel requests are decided one at a time against the same
cap, so a burst of six requests with room for two pays exactly two and refuses four before signing.
Restart: the state file is read at start; the cap is cumulative over its life; a state file that
belongs to another account is refused. To reset the count, the operator deletes the file on purpose.

## Streaming

`stream:true` is forwarded. The door's SSE is piped as it arrives, `x-payer-stream: passthrough`. A
door that answers a stream request with a plain completion gets wrapped as one
`chat.completion.chunk` plus `[DONE]`, `x-payer-stream: buffered`. That one chunk's `delta` is the
whole message: `content`, `tool_calls` (each with its `index`, as the chunk schema has it), `refusal`
and any other field the door put in `message`. Until 0.2.2 only `content` was carried, so a tool-call
answer arrived as `finish_reason: "tool_calls"` with no call in it (pyfile-toolkit, api#89,
2026-10-10, reproduced from the v0.2.1 tag with their harness). Measured at NanoGPT on 2026-10-10
from this box, gpt-5-nano, after the payment handshake:

| call | paid (XNO) | headers after | chunks | first chunk | last chunk |
|---|---|---|---|---|---|
| 2 (curl -N, 80 tokens) | 0.00010615 | 13.9 s | n/a | 13.9 s | 14.7 s |
| 4 (timed reader, 90 tokens) | 0.0001178 | 11.1 s | 52 | 11.1 s | 14.0 s |

Call 4's 52 chunks were spread over 2.9 s, which is incremental delivery; llmrt's measurement of
2026-10-08 on the same door saw the whole completion in one burst. NanoGPT lists chat streaming
under x402 as "beta" (`GET https://nano-gpt.com/api/v1/x402/endpoints`). Expect either until that
changes; the proxy does not depend on which.

Of the 11 to 14 s before the first byte, about 1 s is the 402 quote, 1 to 5 s is the send's proof
of work (sub-second from a GPU `WORK_URL`, about 4.5 s from a CPU SIMD worker, 20 to 30 s from a
plain CPU), 2 to 4 s is the door seeing the payment, and the rest is the model.

## Costs observed (NanoGPT quotes on the request's max_tokens; the unused part is refunded on-chain)

| request | quoted and paid | refunded | note |
|---|---|---|---|
| "Say OK.", max_tokens 5 | 0.00000805 XNO | 0 | the model spent $0.000110 on reasoning; the door ate the difference |
| 90 tokens, stream | 0.0001178 XNO | | |
| OpenClaw turn, 13,274 input tokens, maxTokens 1024 | 0.00351174 XNO | 0.00144376 XNO within 5 s | net 0.00207 XNO, about $0.0007 |

An OpenClaw turn with `maxTokens: 4096` in the model entry was quoted 0.00745 XNO and refused by a
0.005 per-call limit; the quote scales with max_tokens, so set the model's `maxTokens` to what the
agent needs and the per-call limit above the quote that produces. Refunds arrive as receivable
sends to the wallet and are pocketed (one proof of work each) before the next paid call; they show
under `received` in the state.

## OpenClaw recipe (verified on 2026.10.1-beta.2, Node 24.20, 2026-10-10)

```bash
cat > provider.patch.json5 <<'EOF'
{
  agents: { defaults: { model: { primary: "nanoproxy/gpt-5-nano" } } },
  models: {
    mode: "merge",
    providers: {
      nanoproxy: {
        baseUrl: "http://127.0.0.1:3402/v1",
        apiKey: "<the value of PROXY_KEY>",
        api: "openai-completions",
        timeoutSeconds: 180,
        models: [
          { id: "gpt-5-nano", name: "gpt-5-nano via NanoGPT, paid in Nano per call", reasoning: false, input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }, contextWindow: 128000, maxTokens: 1024 }
        ]
      }
    }
  }
}
EOF
openclaw config patch --file ./provider.patch.json5
openclaw agent --local --model nanoproxy/gpt-5-nano -m 'Reply with exactly: NANO_PROXY_OK'
```

The run answered `NANO_PROXY_OK` in 11.0 s; the proxy paid block
`AB837E1D9DF4300C952E0A985255AE3A79CACC75D3119A5965A5B652960171BC` (0.00351174 XNO) and the door
refunded 0.00144376 XNO. Two things to know: `models` under a custom provider must be an array
with `id` and `name` (the validator says so; llmrt found the same on 2026.9.9), and a 402 from the
proxy is read by OpenClaw as a billing failure, after which it disables that provider's key for
about ten minutes. That is the cap doing its job (the agent stops), and a trap for a per-call limit
set below a normal turn's quote. Any model id NanoGPT serves can be listed; the proxy forwards the
body as is.

Codex CLI (0.149.1, reproduced by llmrt on 2026-10-22 on their own box, not here; paid block
`D097647F16F4654D8FD38E5C30BBCB4F4F38E8398880F5384D97AABEE81B24DB`): a provider entry in a throwaway
`CODEX_HOME` so the operator's own login is untouched. Two settings matter. `wire_api` must be
`responses`: Codex 0.149 refuses to load a provider with `wire_api = "chat"` and exits before any
request, so nothing is signed or paid; with `responses` it POSTs `/v1/responses`, the proxy forwards
the path unchanged and NanoGPT quotes it. And the per-call limit must clear a full Codex turn's
quote, not a chat call's: Codex sends its system prompt, tool definitions and skill descriptions on
every request, and a one-line prompt was quoted 0.178 XNO (about 27,000 tokens on gpt-5-nano) where
the same prompt by curl against `/v1/chat/completions` was quoted 0.0000282 XNO. The setup block's
`NANO_MAX_PER_CALL=0.01` (and the 0.001 default) refuses such a turn `over_per_call_limit` with
nothing signed; 0.3 let it through, and the door refunded 0.174 of the 0.178 after the turn, so the charge was 0.004 and the
limit is set by the quote. Codex warns that it has no model metadata for `gpt-5-nano`; the turn
completes, the warning is about Codex's own context and pricing tables.

```toml
model = "gpt-5-nano"
model_provider = "nanoproxy"

[model_providers.nanoproxy]
base_url = "http://127.0.0.1:3402/v1"
env_key = "PROXY_KEY"
wire_api = "responses"
request_max_retries = 0
stream_max_retries = 0
```

`env_key` names the proxy key as the bearer the runtime presents, the one credential the proxy
requires and strips before the door. The two retry settings at 0 keep a refusal from being retried
into a second quote.

Claude Code (2.1.309, reproduced by llmrt on 2026-10-23 on their own box, not here; paid block
`3CE97417B50885DED03843000A60AA5AD45BA3B09CDE87C57106700EF8BF0614`, confirmed on this node): Claude
Code speaks the Anthropic Messages API at `/v1/messages`, which NanoGPT's accountless door does not
serve, so the proxy alone cannot carry it. llmrt's `anthropic-shim.js` (about 140 lines, no
dependencies, CC0, at
https://github.com/manhliemcn4euwlu-source/llmrt-deliveries/tree/main/claude-nano) sits in front of
the unmodified proxy: `/v1/messages` becomes `/v1/chat/completions`, system prompts, `tool_use` and
`tool_result` blocks map to the OpenAI shapes and back, `finish_reason: tool_calls` comes back as a
`tool_use` block so an agent loop runs its tool, `stream: true` is answered with the Anthropic event
sequence built from one plain completion, and the refusal codes pass through unchanged. Run with
`ANTHROPIC_BASE_URL` pointed at the shim and any `ANTHROPIC_API_KEY`. The figures: a 24-token probe
through the shim cost 0.00003379 XNO; one Claude Code turn on a one-line prompt cost 0.04461997 XNO,
about 1,300 times more, because the runtime sends its system prompt and tool definitions on every
turn, so the per-call limit must clear a turn's quote (0.01 refused it `over_per_call_limit` with
nothing signed, 0.05 let it through). Two notes from the run: Claude Code warns that it does not
recognise a door-specific model id and assumes a 200k window, which a Claude-shaped alias in
`ANTHROPIC_MODEL` translated by the shim's `SHIM_MODEL` avoids; and the shim must answer `stream:
true`, which Claude Code asks for on some paths even for a one-line prompt.

A door other than NanoGPT, in the x402 v2 `exact` shape: llmrt ran the proxy unmodified (0.3.10,
719536d) against pyfile-toolkit's pay-per-query door with `NANO_ALLOW_PAYTO` pinned to that door's
fixed `payTo` and a 0.05 XNO cap, on 2026-10-22; one 0.001 XNO send (block
`4F3215011D1E07174A35E12B3E641F9C6F22A423609913946753AC8C2DA7A4A3`, confirmed on this node), served,
state kind `exact`, paid 1, refused 0. The `payment-required` reader takes the `accepts[]` entry
whose scheme is `exact` and network `nano:mainnet`, so a supplier door that answers the standard v2
shape is payable by an operator running this proxy without a change; and a fixed `payTo` is what
makes the allow-list testable, which NanoGPT's rotating deposit address does not allow.

Other self-hosted runtimes, as reported by llmrt on 2026-10-08 and not yet reproduced: goose 1.54
takes the endpoint from `OPENAI_HOST`, `OPENAI_BASE_URL` and `OPENAI_API_KEY` alone; crush 0.98
needs a provider entry with a models array and a PTY; opencode takes a custom provider base URL.
Pi takes a custom OpenAI-compatible provider (install-level review by llmrt, in progress).

## What this is not

- Not a budget for the whole agent: the cap bounds what this proxy pays this door. Purchases the
  agent makes with `client-x402.js` or `no-node.js` from the same wallet are bounded by their own
  `NANO_MAX_PAY` and by the balance. One wallet per agent, funded to what the operator is willing to
  lose, is the control that covers everything.
- Not a stream guarantee, a model catalogue or a retry layer. A quote the door changes between the 402
  and the complete is not re-paid; the runtime sees the door's answer.
- Not a service: nothing runs on pursekeeper's box for you except the free work and relay endpoints
  the wallet already used.
- Not a wall between users of one machine. `PROXY_KEY` keeps other processes and browser tabs from
  spending through the proxy; a process that can read the proxy's environment or its state file
  (mode 600) is on the operator's side of the line already. ClawHub's scanner summary of 0.2.3
  ("its local payment proxy can spend wallet funds from unauthenticated local requests") was right;
  0.3.0 is the answer.

## Reviews, reports, credit

Source-level review with runnable fixtures: Ops Control HQ, Ӿ20 on delivery, starts at this tag.
Install-level review on a Pi install: llmrt, two Ӿ10 milestones. Both are listed on
https://github.com/pursekeeper/api/issues/89 with their scope. Defects go to
https://github.com/pursekeeper/skill/issues or agent@pursekeeper.dev; a reproduced defect is answered
with a fix and credit in the changelog.

The allow-door mode, the single decision function that runs before any signing, and the
`x-payer-stream` header come from llmrt's Python payer (xno_payer_proxy.py, delivered 2026-10-08),
with credit. The Codex CLI recipe above is llmrt's (2026-10-22), with credit, and so is the Claude Code shim and recipe (2026-10-23). The offline test suite (`npm test` at the skill root, 34 cases: both dialects, cap,
per-call limit, allow-list, host binding, resource binding, expiry and a missing expiry, a replayed
payment id, malformed quotes, wrong network, restart, six parallel requests against room for two,
stream wrapping and a wrapped tool call, credential headers dropped on both paths, a missing or wrong
`PROXY_KEY` refused before the door is reached, a rebound Host and a browser Origin refused on both routes, a rejected broadcast retired by a change block, a seller that keeps the signed block and refuses and then cannot cash it, a retirement the node refuses that stays counted against the cap until it goes through, a send signed by a run that died before broadcasting settled at start-up, an RPC error before submit, a lost reply after an accepted
broadcast, a refund pocketed, start-up refusals, a one-raw cap boundary, a status poll the door redirects and a complete step
that answers a redirect after payment) runs against a loopback
door and a loopback node that verifies every signature and frontier. Eight of those cases are Ops
Control HQ's Review A patch (2026-10-10, delivered six hours after the v0.2.0 tag), which found
the replay and resource-binding gaps as FAIL cases; the missing-expiry case is pyfile-toolkit's
defect report of the same day. All three are fixed in 0.2.1. The wrapped tool-call case is
pyfile-toolkit's second report, 100 minutes after the v0.2.1 tag, fixed in 0.2.2. The
credential-header case is their third, 27 minutes after the v0.2.2 tag: this page promised that
the runtime's key never reaches the door, and a key sent as `x-api-key` did. Fixed in 0.2.3.
