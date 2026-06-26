# Runtime Guardrails

This document keeps runtime rules, gates, and scheduled-flow behavior out of the main `SKILL.md` while preserving the actual execution contract.

## Core principle

Host model first, execution scripts first.

- the host model handles product understanding, marketing interpretation, creator-fit reasoning, thread understanding, personalization, and reply judgment
- the scripts handle payload compilation, WotoHub API execution, inbox operations, reply execution, and state persistence
- the skill should not pretend to have an independent built-in model layer for production reasoning

## Hard gates

### 1. Understand first, then execute

For `search`, `recommend`, `campaign_create`, `generate_email`, and `monitor_replies`, missing structured understanding should normally produce a blocked or completion-needed state instead of silently downgrading to a local heuristic main path.

For `scheduled_cycle`, missing `hostAnalysis` is also a hard gate for the search leg.

Rules:
- scheduled search must not compile from legacy near-final search fields as the primary path
- if host analysis is available, reuse it and continue
- if a host analysis bridge is configured, request `hostAnalysis` first, then rerun deterministically
- if it is still missing, return `waiting_for_host_analysis`

### 2. Reply understanding is a hard gate

When `scheduled_cycle` detects a reply and needs to decide between auto-reply and summary, valid host-produced `replyModelAnalysis` must exist first.

Rules:
- local rule-based logic may assist with interpretation
- it must not impersonate the production understanding layer
- if analysis is missing, return `waiting_for_host_reply_analysis`

### 3. Field normalization

Recommended request-layer fields:
- `hostAnalysis`
- `productSummary`
- `hostDrafts`
- `replyModelAnalysis`
- campaign cycle write-back: `host_drafts_per_cycle`

The skill may normalize these into internal runtime fields after input parsing.

Practical rule:
- new integrations, new bridge payloads, and new examples should use the canonical request-layer fields above
- compatibility aliases remain accepted for migration only and should not be extended into new contracts
- for the current alias map, see `references/alias-normalization-matrix.md`

Compatibility aliases are migration-only:
- `understanding`
- `modelAnalysis`
- `emailModelDrafts`
- `conversationAnalysis`
- `hostEmailDrafts`

### 4. Scheduled brief schema gate

Before `scheduled_cycle` executes, the brief is validated to reject near-final search payload fields, including:
- `search.blogCateIds`
- `search.keywords`
- `search.advancedKeywordList`
- `search.searchType`
- `regionList`
- `searchPayload`

Scheduled flows should keep semantic inputs and model analysis, then let the standard compiler rebuild WotoHub search parameters at execution time.

## Default behavior

### Send

- `scheduled_cycle` defaults to `scheduled_send`
- `scheduled_send` is the default real-send path for scheduled flows unless the caller explicitly changes policy or requires review
- `single_cycle` and manual one-off runs default to `prepare_only`
- if `review_required=true`, silent send is not allowed

### Replies

- `scheduled_cycle` defaults to `safe_auto_send`
- only low-risk informational replies may auto-send
- medium and high-risk replies should be converted into summaries for human review

### Success semantics

The following states should not be treated as fully successful completion:
- `needs_user_input`
- `waiting_for_host_analysis`
- `waiting_for_external_host_analysis`
- `waiting_for_host_drafts`
- `waiting_for_host_reply_analysis`
- `review_required`

## Scheduled host bridge patterns

When scheduled execution needs host artifacts, there are valid bridge patterns for `hostAnalysis`, `hostDrafts`, and `replyModelAnalysis`.

### A. Search understanding bridge

Best for cron or external schedulers that want the cycle runner to stay model-first end to end.

```bash
python3 run_campaign_cycle.py \
  --campaign-id your-campaign-id \
  --brief /path/to/brief.json \
  --mode scheduled_cycle \
  --host-analysis-bridge-executor 'python3 /absolute/path/to/your_bridge_executor.py --input {input} --output {output}' \
  --output /tmp/cycle-result.json
```

The skill continues through this flow:
`hostAnalysis -> standard search compiler -> search -> selected creators -> next cycle steps`

If you want to inspect the request without auto-running a bridge, emit:

```bash
python3 run_campaign_cycle.py \
  --campaign-id your-campaign-id \
  --brief /path/to/brief.json \
  --mode scheduled_cycle \
  --host-analysis-bridge-request /tmp/host-analysis-request.json \
  --host-analysis-bridge-payload /tmp/host-analysis-bridge-payload.json \
  --output /tmp/cycle-result.json
```

### B. Draft bridge

When `draft_policy.mode=host_model_per_cycle`, there are two valid integration patterns.

#### Single-entry automatic bridge

Best for cron or external schedulers.

```bash
python3 run_campaign_cycle.py \
  --campaign-id your-campaign-id \
  --brief /path/to/brief.json \
  --mode scheduled_cycle \
  --send-policy scheduled_send \
  --host-bridge-executor 'python3 /absolute/path/to/your_bridge_executor.py --input {input} --output {output}' \
  --output /tmp/cycle-result.json
```

The skill continues through this flow:
`search -> selected creators -> host bridge executor -> host_drafts_per_cycle -> rerun -> send`

#### Two-step manual bridge

Best for debugging or validation.

Step 1, run the cycle and emit bridge payload:

```bash
python3 run_campaign_cycle.py \
  --campaign-id your-campaign-id \
  --brief /path/to/brief.json \
  --mode scheduled_cycle \
  --send-policy prepare_only \
  --host-bridge-request /tmp/host-request.json \
  --host-bridge-payload /tmp/host-bridge-payload.json \
  --output /tmp/cycle-result.json
```

Step 2, let the host consume the payload and produce drafts:

```bash
python3 scripts/host_model_bridge_executor_example.py \
  --input /tmp/host-bridge-payload.json \
  --output /tmp/host-drafts.json
```

Step 3, inject drafts and rerun:

```bash
python3 run_campaign_cycle.py \
  --campaign-id your-campaign-id \
  --brief /path/to/brief.json \
  --mode scheduled_cycle \
  --send-policy prepare_only \
  --host-bridge-drafts /tmp/host-drafts.json \
  --output /tmp/cycle-result-rerun.json
```

## Release hygiene

Before publishing:
- keep `state/` out of source distribution
- remove `.DS_Store`, `__pycache__`, and `*.pyc`
- do not leave local `*.skill` build artifacts inside the source tree
- prefer `WOTOHUB_STATE_DIR` for runtime data
