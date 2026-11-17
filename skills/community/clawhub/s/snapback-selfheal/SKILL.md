---
name: snapback
version: 1.8.4
description: >
  Diagnose why an AI-agent run failed and get a structured fix — and catch failures live, mid-run, before
  they burn your budget. Use this skill WHENEVER an agent run loops, stalls, hits a step/token/context limit,
  returns the wrong output, or fails and you want to know WHY and HOW to fix it. Also use it DURING a run:
  detect_loop and budget_guard catch a runaway before the step limit; a live session streams your steps and
  warns you in real time. Triggers: "why did my agent fail", "it keeps looping", "diagnose this run", "the
  agent repeated the same tool call", "hit the step limit", "running out of context", "burning tokens",
  "wrong output", "detect a loop", "watch my run", "check my agent before running". Connects over MCP; most
  tools are free (discovery, docs, loop + budget checks, live sessions, and instant infrastructure-error
  diagnosis across 46 families), diagnosis is metered (token or pay-per-call via x402 on Solana or EVM — no
  account needed).
homepage: https://snapback.sh
license: MIT
metadata:
  openclaw:
    primaryEnv: SNAPBACK_TOKEN
    envVars:
      - name: SNAPBACK_TOKEN
        required: false
        description: >
          Bearer token (vdk_...) from your https://snapback.sh dashboard. Needed only for diagnose_trace /
          diagnose_batch / get_verdict / submit_feedback / agent_memory / preflight. Discovery, search_docs,
          detect_loop, budget_guard, convert_trace, request_pattern, and live sessions all work with NO token.
    mcp:
      endpoint: https://api.snapback.sh/mcp
      transport: streamable-http
      auth:
        type: bearer
        env: SNAPBACK_TOKEN
---

# Snapback — AI agent failure diagnosis + live guardian

**When it earns its keep:** diagnose the HARD failures — complex, multi-agent, or subtle ones with no clear error message. For a failure whose error message already says what's wrong, just read your logs. The free mid-run guards (detect_loop, budget_guard) cover the frequent cheap cases, so you only pay to diagnose the ~30% that would otherwise cost you hours.

Snapback tells you **why** an agent run failed and **how** to fix it — and can watch a run **as it happens** and
warn you in real time. It's a standard MCP server (Streamable HTTP), so **any MCP-capable agent** connects and
calls its tools — OpenClaw, GitHub Copilot, Hermes (Ollama/vLLM), Claude / Claude Code, Cursor, OpenAI Agents,
or a custom client.

**Why it's safe to trust with your runs:** diagnosis is **library-first** — a known error returns a curated,
verified fix with **no LLM call** in sub-150ms (an LLM-assisted fallback runs only when the library has no match,
and its fixes are never auto-applied). The self-heal gate **auto-applies only reversible, high-confidence library
fixes** (retry/refetch/config) and **escalates every state-changing action — payments, auth, mutations, anything
destructive — to a human, at any confidence**, so it's safe to run unattended. The plugin is **client-side and
zero-dependency**; you send only the error/step structure you pass it, and Snapback **scrubs secret patterns
server-side** as well. Independently evaluated **4.5/5, "approve for production,"** with the on-chain payment path
verified live. MIT-licensed client, hosted service — you can read exactly what the interceptor does before enabling
`auto_apply`.

## Connect

- **Endpoint:** `https://api.snapback.sh/mcp` (Streamable HTTP / JSON-RPC 2.0)
- **Discovery:** `https://snapback.sh/.well-known/mcp.json` (tool list + schemas) · machine guide: `https://snapback.sh/llms.txt`
- **Auth:** `Authorization: Bearer $SNAPBACK_TOKEN` for the metered tools. Everything else is free, no token.

**Calling a tool — IMPORTANT.** The only top-level JSON-RPC methods are `initialize`, `tools/list`, and
`tools/call`. Call every tool through `tools/call` — never as a top-level method (that returns `-32601 method
not found`):
```json
{"jsonrpc":"2.0","id":1,"method":"tools/call",
 "params":{"name":"diagnose_trace","arguments":{"trace":{"...":"..."}}}}
```
The result is in `result.content[0].text` as a JSON string — parse it.

**Latency / treat diagnose as async.** Known patterns return library-instant (<1s, no LLM). A NOVEL failure
needs an LLM call and can take up to ~25s — set your client timeout to **>=30s** and don't block your run loop
on it. The mid-run guards (`detect_loop`, `budget_guard`) and `diagnose_infra_error` are always <1s.

- **Production (recommended):** pay-per-call via **x402** at `/mcp/x402` — no account, no limits. POST a trace,
  get an HTTP 402, pay ~$0.0032 USDC from your wallet, get the verdict. **Works on both Solana and EVM chains**
  (Base and other EVM networks); pick the chain your agent already runs on.
- **Validating first?** Self-register for a starter allowance: `POST https://api.snapback.sh/v1/agents/register`
  with `{"name":"my-agent","framework":"openclaw","accepted_terms":true}` (accepted_terms required — agrees to
  https://snapback.sh/legal/terms). Returns a token; store it as `SNAPBACK_TOKEN`.

Register it once:
```
openclaw mcp add snapback --transport streamable-http --url https://api.snapback.sh/mcp \
  --header "Authorization: Bearer $SNAPBACK_TOKEN"
openclaw mcp reload
openclaw mcp probe snapback   # confirm the tools are exposed
```

## Tools

| Tool | Auth | Metered | When to use |
|------|------|---------|-------------|
| `search_docs(query)` | none | no | Learn the trace format / taxonomy / pricing / free-vs-metered. Call first if unsure. |
| `detect_loop(steps, threshold?)` | none | no | **Mid-run**: are you repeating a tool call? Catch a loop before the step limit. |
| `budget_guard(...)` | none | no | **Mid-run**: context / token / cost / step guards with concrete suggested actions. No LLM. |
| `convert_trace(source)` | none | no | Turn raw logs / OTel spans / message lists into a Snapback trace (so you don't hand-craft JSON). |
| `session_start()` | none | no | **Live**: open a session so Snapback watches your run step-by-step. |
| `session_step(session_id, step, counters?)` | none | no | **Live**: report a step, get loop/budget warnings back inline in real time. |
| `session_end(session_id)` | none | no | **Live**: close the session, get a run summary. |
| `agent_memory(limit?)` | token | no | Your recurring failure patterns ("you loop on web_search 40% of the time"). Call before a run. |
| `preflight(agent_stack?, tags?)` | token | no | **Before running**: known failure patterns for your setup. |
| `diagnose_trace(trace)` | token | **yes** | **After a failure**: full verdict — failure_class, root_cause, fix_suggestion, confidence. |
| `diagnose_batch(traces)` | token | **yes** | Diagnose up to 20 traces in one call. |
| `get_verdict(verdict_id\|trace_id)` | token | no | Fetch a prior verdict. |
| `submit_feedback(verdict_id, correct, note?)` | token | no | Rate a verdict (thumbs + optional note). One per verdict. Improves the shared library. |
| `request_pattern(message, kind?)` | none | no | Ask us to add a failure pattern, or report a problem we couldn't solve. |
| `get_request_status(request_id)` | none | no | Check what happened to a pattern you requested (pending/approved/in_library). |
| `my_impact()` | token | no | How your feedback + requests shaped the shared library. |
| `my_usage()` | token | no | Your used/remaining allowance + estimated spend, so you can self-govern. |

## Free instant fix for cryptic infra errors (diagnose_infra_error)

`diagnose_infra_error({error, context?, action?})` is **free and needs no token** (library-first: a known error returns with no LLM call; a novel one falls back to LLM-assisted diagnosis, never auto-applied). Hand it a
cryptic infrastructure error and it returns the matching family + verified fix instantly from a curated library (no LLM; LLM fallback only on a miss), across **46 families**:
payments (x402, EIP-3009, CCTP, Stripe declines + SCA/3DS/webhook), banking (ACH/NACHA/Plaid), on-chain (Solana,
Token-2022, EVM & Phantom wallets), protocol (MCP, RPC, Airnode, gRPC), infra (database, container-OOM,
cloud-teardown, filesystem, concurrency, DNS/TLS/certs), cloud-native (Kubernetes ImagePullBackOff/admission/
scheduling, Istio/Envoy service-mesh 503-flags, AWS Lambda serverless throttle/DLQ), infra-as-code (Terraform
state-lock/drift), messaging (Kafka/SQS, Twilio A2P 10DLC SMS 30007/30034), data (type-encoding, vector-db,
webhook-drift, Snowflake/Databricks warehouse), cache (Redis maxmemory/cluster MOVED-ASK), search (Elasticsearch
circuit-breaker), graphql (GitHub + generic cost-based GraphQL 200-RATE_LIMITED/THROTTLED), enterprise (CRM-sync, Shopify/Amazon commerce, calendar-ETag, Microsoft
Graph/Entra), identity (Persona/Alloy/Socure KYC), ci-cd (GitHub Actions permissions/runners), healthcare (X12
837/835/277CA EDI), ad-tech (OpenRTB no-bid/loss), travel (Amadeus/Sabre GDS), and auth (OAuth, JWT/AWS-SigV4,
vendor/LLM-API quirks, LLM-output truncation). Many share a "200-OK-is-a-lie / false-success" pattern (the op
returns success but silently failed — GraphQL THROTTLED, Twilio queued-then-filtered, Lambda async-to-DLQ, EDI
999-then-277CA-reject). Call it the moment you hit an error you can't instantly solve — the cheapest self-correct.

```
diagnose_infra_error({error: "unable to get local issuer certificate"})
# -> { matched: true, family: "dns-tls", root_cause: "...", fix: "serve the intermediate cert chain", confidence }
```

## Self-heal automatically (the plugin) — run it on EVERY error, not just when you remember

`pip install snapback-selfheal`. Wrap your tool calls and it auto-diagnoses every error and applies the safe fix,
gated. This is the difference between a tool you decide to reach for and infrastructure that runs reflexively:

> **Installing this skill via ClawHub:** `clawhub install snapback-selfheal` installs into the *current
> directory* (`./skills/`), so run it from your OpenClaw workspace root (or `cd ~/.openclaw` first) — running it
> from a scratch dir puts the skill where your agent can't see it (it won't show in `available_skills`). The
> `pip install snapback-selfheal` above is separate and installs the interceptor package normally.


```python
from snapback_interceptor import SnapbackInterceptor
heal = SnapbackInterceptor(auto_apply=True)
result = heal.run(my_tool_call, *args, **kwargs)   # on error: auto-diagnose, safe-retry once, else escalate
```

**The autonomous-action GATE CONTRACT** (why it's safe to run unattended). Every verdict returns
`{source, confidence, action_class, auto_safe, gate:{auto_apply_ok}}`. The interceptor auto-applies a fix ONLY when:
`source == "library"` AND a reversible `action_class` (retry/refetch/config) AND `confidence >= the per-class threshold` (config 0.80, refetch 0.82, retry 0.85) (a curated verified fix, not an LLM guess) AND `auto_safe == true`
(action_class is retry|refetch|config — reversible). It NEVER auto-applies a `mutate`/`destructive` fix (anything
that creates/changes state, money, or auth) — those escalate to a human. **Defense in depth (1.8.3): even a
reversible-class fix is down-graded to escalate if its text contains a destructive command** (e.g. delete a pod,
flush keys, drop a table) — the gate returns `gate.contains_destructive_step`, so a fix can never auto-run a
state-destroying step regardless of its class. Fails closed: when unsure, escalate. You can read
`gate.auto_apply_ok` directly to decide.

**The crowd view (`what_others_did`)** — once you've diagnosed a failure_class, ask what fix worked for other
agents that hit the same thing: an anonymized success-rate + the fixes that actually resolved it. Report your own
outcome with `report_outcome` so the library gets sharper for the next agent. (These sharpen as adoption grows.)

## The trace format (for diagnose_trace)

Tolerant — send what you have; `steps` matter most. A worked example:
```json
{"trace": {
  "trace_id": "loop-001", "agent": "my-agent", "final_status": "failed",
  "steps": [
    {"index": 1, "action": "web_search", "inputs": {"query": "X"}, "status": "success"},
    {"index": 2, "action": "web_search", "inputs": {"query": "X"}, "status": "success"},
    {"index": 3, "action": "web_search", "inputs": {"query": "X"}, "status": "success"},
    {"index": 4, "action": "step_limit", "error": "Step limit exceeded", "status": "failed"}
  ]}}
```
Field names are flexible: `index|step|i`, `action|tool|operation`, `inputs|arguments`, `outputs|result`,
`status`, `error`. Content in inputs/outputs is redacted server-side — you don't pre-redact. The verdict
returns a real `id` you can then pass to `get_verdict` / `submit_feedback`.

## Usage examples

**1. Diagnose a failed run**
```
diagnose_trace({trace: { final_status: "failed", steps: [
  {index:1, action:"web_search", inputs:{query:"X"}, status:"success"},
  {index:2, action:"web_search", inputs:{query:"X"}, status:"success"},
  {index:3, action:"step_limit", error:"limit", status:"failed"} ]}})
# -> { id, failure_class: "loop_repeated_tool_call", root_cause, fix_suggestion, confidence }
```

**2. Catch a loop mid-run (free)**
```
detect_loop({steps: [ {action:"web_search",inputs:{query:"X"}}, {action:"web_search",inputs:{query:"X"}},
                      {action:"web_search",inputs:{query:"X"}} ]})
# -> { looping: true, offending_action: "web_search", suggestions: [...] }
```

**3. Live guardian — stream a run and get warnings in real time (free)**
```
{session_id} = session_start()
session_step(session_id, {action:"web_search", inputs:{query:"X"}}, {tokens_used: 8000, token_budget: 10000})
# ... after 3 identical steps -> { warnings: [{type:"loop", ...}] }
# ... near budget -> { warnings: [{type:"token_burn", severity:"critical", suggestions:[...]}] }
session_end(session_id)   # -> { summary }
```

## Paying

- **Token (subscription):** your `vdk_` token meters `diagnose_trace` against your plan (Free 2000/mo).
- **Pay-per-call (x402):** no subscription — POST your `{"trace": {...}}` to `https://api.snapback.sh/mcp/x402`
  with no token. You get **HTTP 402** with the USDC contract, EIP-712 domain, payTo, amount (~$0.0032), and
  facilitator. Sign an EIP-3009 authorization and retry with the signed payment in the **`PAYMENT-SIGNATURE`**
  header (`X-PAYMENT` also accepted). An empty/unreadable trace is **never charged**. Supported on **Solana and
  EVM chains** — each chain has its own receiving address; your agent pays from the wallet it already uses.
- **No wallet / can't sign?** You do **not** need to pay to start. POST `/v1/agents/register` with
  `accepted_terms=true` for a **free starter-allowance token** — no crypto stack needed. Move to x402 later once
  you have a funded wallet. (Hitting a 402 you can't complete is itself diagnosable: `diagnose_infra_error("402
  can't sign no wallet")` returns this exact guidance.)

**Self-hosted (coming):** a self-hostable Snapback for teams with data-residency or air-gap requirements is on
the way — run the diagnosis engine inside your own environment. Ask via `request_pattern` if you need it.

## Security & data handling

- Trace content is redacted before the engine sees it: credential fields (password/api_key/token/secret/...)
  are masked and secret patterns (sk-/AKIA/Bearer/JWT) are scrubbed anywhere they appear. Responses are
  sanitized so no secret-shaped string is returned.
- Tokens are org-scoped: an agent only reads/writes its own org's data.
- Best practice: keep your token in SNAPBACK_TOKEN (never in a prompt or committed file); don't put raw
  credentials in a trace - send the structure of what happened, not your keys.
- This skill only talks to snapback.sh. It runs no shell commands, reads no files, and installs nothing.
