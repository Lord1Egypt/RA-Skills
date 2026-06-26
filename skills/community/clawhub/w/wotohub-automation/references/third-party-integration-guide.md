# Third-Party Integration Guide

This is the fastest way to make `wotohub-automation` feel plug-and-play for external users.

## Goal

Set default host executors once in your wrapper / launcher environment, then let the skill auto-discover them.

That gives you:
- URL product recovery without every caller passing `hostAnalysisExecutor`
- reply understanding without every caller passing `hostReplyAnalysisExecutor`
- draft generation without every caller passing `hostDraftExecutor`

## Recommended environment defaults

Simplest setup: point all three env vars at the single router.

```bash
export WOTOHUB_HOST_ANALYSIS_EXECUTOR='python3 /ABS/PATH/host_executor_router.py --input {input} --output {output}'
export WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR='python3 /ABS/PATH/host_executor_router.py --input {input} --output {output}'
export WOTOHUB_HOST_DRAFT_EXECUTOR='python3 /ABS/PATH/host_executor_router.py --input {input} --output {output}'
```

If you prefer separate executors, these also work:

```bash
export WOTOHUB_HOST_ANALYSIS_EXECUTOR='python3 /ABS/PATH/host_analysis_executor_example.py --input {input} --output {output}'
export WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR='python3 /ABS/PATH/host_reply_analysis_executor_example.py --input {input} --output {output}'
export WOTOHUB_HOST_DRAFT_EXECUTOR='python3 /ABS/PATH/host_draft_executor_example.py --input {input} --output {output}'
```

Compatibility aliases also work:
- `HOST_ANALYSIS_EXECUTOR`
- `HOST_REPLY_ANALYSIS_EXECUTOR`
- `HOST_DRAFT_EXECUTOR`

## Discovery order

### 1. Product understanding / URL recovery
1. `config.hostAnalysisExecutor`
2. `brief.hostAnalysisExecutor` / `brief.scheduler.hostAnalysisExecutor`
3. `WOTOHUB_HOST_ANALYSIS_EXECUTOR`

### 2. Reply understanding
1. `config.hostReplyAnalysisExecutor` / `config.hostReplyBridgeExecutor`
2. `brief.scheduler.hostReplyBridgeExecutor`
3. `WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR`

### 3. Host draft generation
1. `config.hostDraftExecutor` / `config.hostBridgeExecutor`
2. `brief.scheduler.hostBridgeExecutor`
3. `WOTOHUB_HOST_DRAFT_EXECUTOR`

## What each executor receives and returns

### Product understanding executor
Receives:
- `host_analysis_request`
- `host_url_analysis_request`

Should return:
```json
{
  "hostAnalysis": {},
  "productSummary": {}
}
```

Reference schema:
- `references/model-analysis-schema.md`

Recommended starter:
- `scripts/host_executor_router.py`
- `scripts/host_analysis_executor_example.py`

### Reply understanding executor
Receives:
- `host_reply_analysis_request`

Should return:
```json
{
  "replyModelAnalysis": {
    "items": []
  }
}
```

Reference schema:
- `references/conversation-analysis-schema.md`

Recommended starter:
- `scripts/host_executor_router.py`
- `scripts/host_reply_analysis_executor_example.py`

### Draft generation executor
Receives:
- `host_draft_request`
- campaign bridge draft payloads when applicable

Should return:
```json
{
  "hostDrafts": [],
  "writeBackMetadata": {}
}
```

Reference schema:
- `references/outreach-email-schema.md`

Recommended starters:
- `scripts/host_executor_router.py`
- `scripts/host_draft_executor_example.py`
- `scripts/host_model_bridge_executor_example.py` (cycle-oriented bridge example)

## Minimal wrapper pattern

### Option A: zero-thinking launcher for generic requests

Use:

```bash
python3 run_skill_with_router.py --request-path /path/to/request.json
```

Behavior:
- auto-wires the three router-based env defaults if they are missing
- forwards the request to `wotohub_skill.py`
- preserves any explicit env overrides you already set

### Option B: zero-thinking launcher for cycle runs

Use:

```bash
python3 run_cycle_via_skill.py --campaign-id demo-campaign --brief-path /path/to/brief.json --mode scheduled_cycle
```

Behavior:
- auto-wires router-based env defaults before invoking `wotohub_skill.py`
- keeps the cycle request on the canonical campaign entry path

### Option C: custom shell wrapper

If you prefer your own launcher, set the env defaults yourself.

Example:

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="/path/to/wotohub-automation"
export WOTOHUB_HOST_ANALYSIS_EXECUTOR="python3 $ROOT/scripts/host_executor_router.py --input {input} --output {output}"
export WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR="python3 $ROOT/scripts/host_executor_router.py --input {input} --output {output}"
export WOTOHUB_HOST_DRAFT_EXECUTOR="python3 $ROOT/scripts/host_executor_router.py --input {input} --output {output}"

python3 "$ROOT/wotohub_skill.py"
```

## Practical behavior after setup

### URL product analysis
1. skill tries script-side fetch / parse
2. weak or blocked page -> emits `hostUrlAnalysisRequest`
3. upper layer auto-discovers host analysis executor
4. executor returns `hostAnalysis + productSummary`
5. skill auto-reruns and continues on the normal path

### Reply assist
1. skill sees `replyModelAnalysis` is required
2. auto-discovers reply executor
3. executor returns structured conversation analysis
4. skill continues into preview / policy logic

### Draft generation
1. skill sees host drafts are required
2. auto-discovers draft executor
3. executor returns one draft per selected creator
4. skill continues into preview / send policy logic

## Important rule

Do not return near-final WotoHub search payloads as a substitute for product understanding.

Keep the contract at the semantic layer:
- `hostAnalysis`
- `productSummary`
- `replyModelAnalysis`
- `hostDrafts`

Let the skill own:
- payload compilation
- policy checks
- send / reply execution

## Recommended onboarding note for external users

If you want the easiest first-run experience, ship the skill together with a wrapper that already sets:
- `WOTOHUB_HOST_ANALYSIS_EXECUTOR`
- `WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR`
- `WOTOHUB_HOST_DRAFT_EXECUTOR`

That removes almost all executor-related setup from the caller's mental model.
