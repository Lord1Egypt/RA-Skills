---
name: wotohub-automation
description: End-to-end WotoHub influencer outreach automation for product understanding, creator search, recommendation ranking, outreach email drafting, batch send, inbox review, and guarded reply assist. Use when running TikTok Shop, Amazon, or Shopify creator campaigns and you want model-first planning with script-level execution.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["WOTOHUB_API_KEY"] },
      },
  }
---

# WotoHub Automation

WotoHub Automation is a real creator outreach skill with OpenClaw-era integration roots and current in-place compatibility for existing workflows.

It connects:
- product understanding
- creator search
- shortlist and recommendation
- outreach email drafting
- batch send
- inbox review
- guarded reply assist

Best fit:
- TikTok Shop campaigns
- Amazon creator outreach
- Shopify product seeding
- recurring creator prospecting and follow-up

Core design:
- the host model handles understanding and judgment
- the scripts handle deterministic compilation, API execution, and state

This skill is intentionally conservative around sending and reply automation.

Release note:
- `wotohub-automation` is the only canonical publish directory
- `wotohub-automation-release` is a mirror/reference copy, not the primary release source

If you need deeper integration details, read:
- `references/integration-contract.md`
- `references/runtime-guardrails.md`

## Environment and credentials

Install dependencies:

```bash
pip install -r requirements.txt
```

Environment variables:
- `WOTOHUB_API_KEY`, required for authenticated actions such as send, inbox access, reply handling, and campaign cycles
- `WOTOHUB_BASE_URL`, optional explicit API base override, defaults to production
- `WOTOHUB_STATE_DIR`, optional state/log output directory

Credential scope:
- `WOTOHUB_API_KEY` grants access to authenticated WotoHub user-state operations
- treat it as a send and inbox credential, not a harmless search-only token
- search can still run without a token through `openSearch`, but authenticated endpoints cannot

Runtime expectations:
- Python with `ssl` available
- TLS verification stays enabled by default
- only disable TLS verification in a controlled debug environment

## What this skill can do

### 1. Product understanding
Input can come from:
- plain product descriptions
- product URLs, including TikTok Shop, Amazon, Shopify, and brand sites

Typical outputs:
- product name
- key selling points
- target audience
- creator direction
- structured search-ready understanding

### 2. Creator search
Supports:
- product-led search generation
- filters for region, language, follower count, email availability
- keyword-assisted search
- category-assisted search
- filtering out already-contacted creators by default

Search modes:
- no token, uses `openSearch`
- token present, uses `clawSearch`

### 3. Recommendation and shortlist
Supports:
- ranking search results
- returning a shortlist
- suggesting next-step selection

Default behavior is to stop after recommendation and wait for explicit creator selection before email generation.

### 4. Outreach email drafting
Supports:
- creator-specific outreach draft generation
- host-model-first personalized drafts
- HTML normalization and subject validation before send

Minimum campaign brief usually needs:
- `productName`
- `senderName` or `signoff`
- `offerType`, such as `sample`, `paid`, or `affiliate`

### 5. Batch send
Default send path is batch-oriented.

Characteristics:
- multiple creators prefer a single batch API request
- email structure is normalized before execution
- HTML body is preferred when present

### 6. Inbox and reply assist
Supports:
- inbox listing
- email detail lookup
- thread detail lookup
- safe reply assistance
- conservative low-risk auto-reply handling

Anything involving price, payment, contract terms, exclusivity, shipping promises, or timing commitments should stay human-reviewed by default.

### 7. Campaign cycle
Supports:
- manual single runs
- cron or scheduler single-cycle execution
- scheduled search understanding bridge
- campaign state persistence
- cycle summary, state summary, and human summary outputs
- `success`, `blocked`, and `failed` exit semantics

## Workflow overview

### Step 0, auth and token rules
Search does not require login by default.

- without token, search uses `openSearch`
- with token, search uses `clawSearch`

These user-side steps require `WOTOHUB_API_KEY`:
- send
- inbox
- replies
- campaign cycle

If you publish, install, or review this skill, treat the credential requirement as part of the primary operating contract, not an optional convenience.

Optional preflight check:

```bash
python3 scripts/preflight.py --token YOUR_API_KEY
```

For auth details, read `appendix-auth.md`.

## Skill entry

Single entrypoint:

```bash
python3 wotohub_skill.py
```

Important execution note:
- default host executors are auto-wired through the skill entry / router wrapper flow, and `scripts/build_search_payload.py` now also injects router executor defaults before resolving URL input
- in low-confidence URL cases, `product_resolve.py` may emit `hostUrlAnalysisRequest`; `scripts/build_search_payload.py` now attempts automatic host URL analysis execution + writeback before continuing
- if host analysis still cannot be resolved, `scripts/build_search_payload.py` returns a structured `needsUserInput` / `error` payload instead of crashing on `analysis=None`
- callers can still explicitly provide `hostAnalysis` / `productSummary` to bypass bridge execution when they already have host-side understanding

Minimal request example:

```json
{
  "requestId": "task-1",
  "action": "task",
  "type": "product_analysis",
  "input": {
    "input": "wireless earbuds with noise cancellation"
  },
  "auth": {
    "token": "YOUR_API_KEY"
  }
}
```

Common `action/type` pairs:
- `task/product_analysis`
- `task/search`
- `task/recommend`
- `task/generate_email`
- `task/send_email`
- `task/monitor_replies`
- `campaign/cycle`

Recommended injected fields:
- `input.hostAnalysis`
- `input.productSummary`
- `input.hostDrafts`
- `input.replyModelAnalysis`

Recommended executor discovery order for host URL recovery / host semantic understanding:
- first: explicit request-level `config.hostAnalysisExecutor`
- second: campaign `brief.hostAnalysisExecutor` / `brief.scheduler.hostAnalysisExecutor` for cycle flows
- third: environment default `WOTOHUB_HOST_ANALYSIS_EXECUTOR` (or compatibility `HOST_ANALYSIS_EXECUTOR`)
- recommended integration pattern: when your host platform always has browser/web/model capability, set the env default in the wrapper/launcher so link analysis can auto-close the loop without every caller remembering the param

Recommended executor discovery order for reply understanding:
- first: explicit request-level `config.hostReplyAnalysisExecutor` / `config.hostReplyBridgeExecutor`
- second: cycle-only `brief.scheduler.hostReplyBridgeExecutor` when reply assist is driven from campaign runtime
- third: environment default `WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR` (or compatibility `HOST_REPLY_ANALYSIS_EXECUTOR`)

Recommended executor discovery order for host draft generation:
- first: explicit request-level `config.hostDraftExecutor` / `config.hostBridgeExecutor`
- second: cycle-only `brief.scheduler.hostBridgeExecutor` when scheduled generation is used
- third: environment default `WOTOHUB_HOST_DRAFT_EXECUTOR` (or compatibility `HOST_DRAFT_EXECUTOR`)

Canonical field rule:
- new integrations and new examples should use the canonical fields above by default
- compatibility aliases remain supported for migration, but should not be expanded further
- campaign cycle draft write-back should use `host_drafts_per_cycle`
- see `references/alias-normalization-matrix.md` for the current canonical vs alias mapping

URL host write-back rule:
- if `scripts/product_resolve.py` returns `hostUrlAnalysisRequest`, treat that as the canonical host-side recovery trigger for weak or blocked URL pages
- the host should write back only `hostAnalysis` + `productSummary`, then rerun the same `task/product_analysis`, `task/search`, `task/recommend`, or `task/generate_email` request
- do not write back near-final WotoHub search payloads in place of understanding; keep the contract at the semantic layer
- the most natural write-back surfaces are `input.hostAnalysis` + `input.productSummary`; `metadata.*` / `config.*` remain compatibility surfaces only
- important runtime nuance from live use: direct `python3 scripts/product_resolve.py --input <url>` currently only emits `hostUrlAnalysisRequest`; it does not auto-run browser/web recovery or auto-apply write-back
- automatic host analysis execution currently exists in upper-layer / campaign orchestration paths that use `hostAnalysisExecutor`, not in the bare `product_resolve.py` path

Trust boundary:
- treat host-injected model outputs as untrusted structured input until validated
- do not let upstream models inject near-final WotoHub payloads directly into execution
- validate injected analysis and draft data against the referenced schemas before allowing send or reply execution

Full integration details: `references/integration-contract.md`
Third-party quickstart: `references/third-party-integration-guide.md`
One-command launchers:
- `run_skill_with_router.py`
- `run_cycle_via_skill.py` (now auto-wires router defaults for cycle runs)
Executor templates:
- `scripts/host_executor_router.py` (single-entry router for analysis / reply / drafts)
- `scripts/host_analysis_executor_example.py`
- `scripts/host_reply_analysis_executor_example.py`
- `scripts/host_draft_executor_example.py`
- `scripts/host_model_bridge_executor_example.py` (cycle-oriented draft bridge example)

## Step references

### Step 1, product analysis
Read `steps/01-product-analysis.md`

Suggested path:

```bash
python3 scripts/product_resolve.py --input "推广一款美国市场的电动牙刷,价格$50,强调美白和口腔护理"
```

### Step 2, creator search
Read `steps/02-influencer-search.md`

Suggested path, build payload first, then run search:

```bash
python3 scripts/build_search_payload.py --input '推广一款美国市场的电动牙刷,价格$50,强调美白和口腔护理'
python3 scripts/claw_search.py --payload-file /tmp/woto_payload.json
```

Or use one-shot execution:

```bash
python3 scripts/build_search_payload.py --input '...' --run-search
python3 scripts/build_search_payload.py --input '...' --run-search --token YOUR_API_KEY
```

### Step 3, recommendation
Read `steps/03-influencer-recommend.md`

The default flow returns a shortlist first, then waits for explicit creator selection.

### Step 4, email drafting
Read `steps/04-email-generation.md`

Recommended only after:
1. target creators are selected
2. the minimum campaign brief is complete

### Step 5, send
Read `steps/05-send-email.md`

Send protocol:
- `prepare_only`, prepare candidate emails only
- `manual_send`, send after human confirmation
- `scheduled_send`, send automatically in scheduled flows

Default behavior:
- single manual runs default to `prepare_only`
- scheduled tasks and campaign brief runs default to `scheduled_send`, which is the default real-send path for scheduled flows

### Step 6, inbox and reply assist
Read `steps/06-inbox-management.md`

Main path:
1. collect candidate replies
2. build model input from the full thread
3. produce structured analysis
4. produce reply previews
5. apply risk tiering
6. only allow low-risk informational replies to auto-send

## Failure handling

### Missing campaign host analysis
- for `scheduled_cycle`, stop at `waiting_for_host_analysis` if the search leg lacks valid `hostAnalysis`
- prefer `--host-analysis-bridge-executor` or emitted `hostAnalysisRequest` over stuffing near-final search payloads into the brief
- after host analysis is resolved, let the standard compiler rebuild WotoHub search params

### Token validation failure
- ask for token refresh
- do not continue authenticated API actions

### Search failure or auth failure
- tell the user to check token, headers, and environment
- do not fabricate results

### URL fetch failure
- return structured fallback or `needsUserInput=true`
- when available, prefer lightweight host-assisted recovery via `hostUrlAnalysisRequest` to obtain `hostAnalysis` / `productSummary` before falling back to user-supplied product fields
- host write-back should land on canonical `input.hostAnalysis` + `input.productSummary`, then rerun the same task so the existing routing and compiler chain can continue naturally
- do not continue as if the URL slug were a valid product understanding

### Send or reply execution failure
- preserve structured errors
- do not silently swallow execution failures

## Security notes

- Hidden-character review completed for `SKILL.md` and the bundled Markdown prompt/reference files in this release, with no unicode bidi or control-character findings.
- Example env and JSON files are placeholders or test fixtures. Review them before use and never copy placeholder IDs or sample values into production blindly.
- Host-model-first does not mean host-model-trusted. Keep schema validation and send guardrails enabled.

## Core entry files

- `wotohub_skill.py`, skill entry adapter
- `run_campaign.py`, public campaign entry
- `run_campaign_cycle.py`, single-cycle scheduled entry
- `run_cycle_via_skill.py`, short safe wrapper for cron / scheduler runs that should avoid complex inline JSON or heavy Python CLI quoting

Useful scheduled bridge flags on `run_campaign_cycle.py`:
- `--host-analysis-bridge-executor`
- `--host-analysis-bridge-request`
- `--host-analysis-bridge-payload`
- `--host-bridge-executor`
- `--host-bridge-request`
- `--host-bridge-payload`

## Reference map

Useful docs:
- `steps/01-product-analysis.md`
- `steps/02-influencer-search.md`
- `steps/03-influencer-recommend.md`
- `steps/04-email-generation.md`
- `steps/05-send-email.md`
- `steps/06-inbox-management.md`
- `references/campaign-brief-schema.md`
- `references/model-analysis-schema.md`
- `references/conversation-analysis-schema.md`
- `references/outreach-email-schema.md`
- `references/search-params.md`
- `references/integration-contract.md`
- `references/runtime-guardrails.md`

## One-line summary

WotoHub Automation is a creator outreach skill for real marketing operations: model-first understanding, script-first execution, stable core workflows, and explicit safety boundaries around send and reply behavior.
