# RSS-Brew Phase A Direct API Migration Plan

**Date:** 2026-03-09  
**Status:** Proposed  
**Target:** Replace Phase A scoring's agent-style model invocation path with a direct DeepSeek API call using `deepseek-reasoner`.

---

## 1. Objective

Migrate RSS-Brew Phase A scoring from its current indirect/orchestrated model invocation pattern to a deterministic, direct LLM API call.

The goal is **not** to redesign the whole pipeline. The goal is to make Phase A:
- faster
- cheaper in framework overhead
- easier to batch / retry / observe
- less dependent on agent/session orchestration

---

## 2. Why Phase A first

Phase A is the best first candidate for direct API migration because it is the most function-like stage in the pipeline.

It already behaves like:

```text
input articles -> score/classify -> scored output JSON
```

Compared with deeper synthesis stages, it has:
- clearer input/output structure
- lower ambiguity
- easier batching
- easier regression comparison
- lower risk of semantic drift

So the migration order should be:

1. **Phase A direct API**
2. validate quality/cost/latency
3. only then consider whether Phase B should also move to direct API

---

## 3. Current State

Today, Phase A scoring lives in:

```text
scripts/phase_a_score.py
```

It is currently called by:

```text
scripts/run_pipeline_v2.py
```

And operationally, the system now runs through:

```text
rss_brew.cli
 -> scripts/run_pipeline_v2.py
 -> scripts/phase_a_score.py
```

The current app/runtime internalization work has already improved orchestration structure, but Phase A still uses a higher-overhead model invocation path than necessary.

---

## 4. DeepSeek API constraints / assumptions

Based on the current DeepSeek docs:

- DeepSeek API is OpenAI-compatible
- Base URL:
  - `https://api.deepseek.com`
  - or `https://api.deepseek.com/v1` for OpenAI-compatible SDK usage
- Model to use for this migration:
  - `deepseek-reasoner`
- `deepseek-reasoner` is the thinking mode variant

This means Phase A can be migrated using either:
- raw HTTP requests
- OpenAI-compatible SDK configured against DeepSeek base URL

### Recommendation
Use the **OpenAI-compatible Python SDK path** if already available in the environment, because it reduces custom HTTP plumbing and keeps the code simple.

If dependency simplicity is more important, raw `requests` is also acceptable.

---

## 5. Migration strategy

### Recommended strategy: internal replacement, interface preserved

Do **not** change the external contract of Phase A first.

Keep:
- `scripts/phase_a_score.py` as the operational entrypoint for now
- current input/output file contract the same
- current orchestrator call site unchanged if possible

Only change the **inside** of Phase A so that scoring uses direct DeepSeek API calls.

This gives you:
- minimal orchestrator impact
- easier rollback
- direct A/B comparison against current behavior

---

## 6. Proposed target behavior

### Input
Still read:
- `new-articles.json`

### Output
Still write:
- `scored-articles.json`

### Internal change
Replace the current model invocation path inside Phase A with:
- direct DeepSeek API call(s)
- model = `deepseek-reasoner`
- explicit timeout / retry / parsing logic
- deterministic JSON extraction

---

## 7. Design choices

## 7.1 Keep Phase A as a bounded service-style stage

Phase A should become a deterministic scoring stage with:
- fixed prompt
- fixed output schema
- explicit parse/validation
- explicit retry behavior

### Recommended output schema per article
At minimum, the LLM should return structured fields like:
- `score`
- `category`
- `reasoning` or short rationale
- optional flags / notes

If RSS-Brew already has a current output shape, preserve it exactly unless there is a strong reason to change it.

---

## 7.2 Prefer one-article-at-a-time first, batch later

For the first migration pass, I recommend:
- **one article per API call**
- preserve ordering
- preserve current limit behavior

Why:
- simpler debugging
- easier comparison against existing behavior
- easier error attribution
- easier rollback

After it stabilizes, Phase A can later add small-batch scoring.

---

## 7.3 Add explicit retry and timeout policy

Direct API means you own the reliability contract.

Recommended minimal policy:
- request timeout: e.g. 60s
- retry count: 2 or 3 on transient failures
- exponential backoff
- log parse failures separately from API failures

Do **not** silently downgrade missing/failed articles into fake successful scores.

---

## 7.4 Add deterministic parse layer

The migration will be much safer if the model is instructed to emit strict JSON.

Recommended approach:
- strong system prompt
- explicit JSON schema in prompt
- parse + validate after response
- if parse fails, retry once with a repair prompt or mark failure clearly

---

## 8. Proposed implementation steps

## Step 1 — Add a dedicated direct-API scoring helper

Create an app-native helper, for example:

```text
app/src/rss_brew/llm/deepseek_phase_a.py
```

Responsibilities:
- build request payload
- call DeepSeek API
- parse/validate response
- return structured scoring result

This is better than putting API details directly into `phase_a_score.py`.

---

## Step 2 — Keep `scripts/phase_a_score.py` as entrypoint

Update `scripts/phase_a_score.py` to call the new helper instead of the current indirect model invocation path.

Why:
- minimal operational change
- orchestrator does not need to change much
- rollback is easy

---

## Step 3 — Add config knobs

Add or standardize configuration for:
- `DEEPSEEK_API_KEY`
- `DEEPSEEK_BASE_URL` (default `https://api.deepseek.com` or `/v1` depending SDK choice)
- model default = `deepseek-reasoner`
- request timeout
- retry count

These can live in env vars first. Do not over-design config in the first pass.

---

## Step 4 — Preserve current CLI and orchestrator contract

Do **not** change:
- `rss_brew.cli run`
- `scripts/run_pipeline_v2.py` Phase A call contract
- data root layout
- Phase A output filename

This keeps the migration bounded.

---

## Step 5 — Add migration-specific tests

You will need at least:
- unit test for prompt/request shaping
- unit test for response parsing
- unit test for malformed JSON handling
- unit test for retry behavior
- regression test that output schema remains compatible

And ideally:
- a fixture-based test with canned DeepSeek API responses

Do **not** make tests depend on live API calls.

---

## 9. Suggested file changes

### Likely new files
- `app/src/rss_brew/llm/deepseek_phase_a.py`
- possibly `app/src/rss_brew/llm/__init__.py`
- test files under `app/tests/` for the helper

### Likely updated files
- `scripts/phase_a_score.py`
- possibly `requirements.txt` if a dependency is needed
- `app/docs/ops-runbook.md` if env/setup instructions change materially
- `docs/rss-brew-implementation-plan.md` after the milestone lands

---

## 10. Acceptance criteria

Phase A direct API migration is successful if:
- Phase A uses direct DeepSeek API calls to `deepseek-reasoner`
- current input/output contract remains stable
- orchestrator continues to run without semantic redesign
- tests cover request/parse/retry basics
- dry-run or controlled validation shows no schema breakage
- a small real run succeeds through the normal pipeline

---

## 11. Risks

### Risk 1 — Score drift
Changing invocation method may change scoring behavior even with similar prompts.

**Mitigation:**
- compare old vs new outputs on a fixed sample set
- keep prompt wording close at first

### Risk 2 — Parse instability
If the model emits non-JSON or malformed JSON, Phase A can become flaky.

**Mitigation:**
- strict prompt
- validation layer
- bounded retry

### Risk 3 — Overusing `deepseek-reasoner`
`deepseek-reasoner` may be slower or more expensive than needed for simple scoring.

**Mitigation:**
- start with it because that is your stated choice
- measure latency/cost after migration
- keep the helper structured so the model can later be swapped to `deepseek-chat` if scoring does not need reasoning depth

### Risk 4 — Hidden coupling in current `phase_a_score.py`
The current file may rely on existing helper patterns more deeply than expected.

**Mitigation:**
- keep the migration internal to Phase A first
- avoid changing orchestrator and file contracts in the same pass

---

## 12. Additional implementation guardrails

Before implementation starts, apply these constraints explicitly:

### Guardrail 1 — Freeze `scored-articles.json` schema
The migration must preserve the current output contract of Phase A.

Do not allow the direct-API migration to casually change:
- field names
- field nesting
- score representation
- category representation
- downstream-required article payload structure

A schema snapshot / concrete example should be reviewed before coding.

### Guardrail 2 — Use one API client strategy in V1
Do not leave the implementation undecided between raw HTTP and multiple client approaches.

For the first migration pass, standardize on:
- **OpenAI-compatible Python SDK against DeepSeek**

unless a concrete environment constraint blocks it.

### Guardrail 3 — Measure `deepseek-reasoner` operational fit
This migration should accept `deepseek-reasoner` as the requested model, but it must record:
- per-article latency
- parse failure rate
- approximate run-time cost profile

If the model proves too slow/heavy for simple scoring, a later follow-up can evaluate a lighter replacement without invalidating the migration structure.

### Guardrail 4 — Audit current Phase A logic before replacement
Before replacing internals, review the existing `scripts/phase_a_score.py` behavior and preserve:
- scoring rubric intent
- category mapping intent
- fallback behavior
- any output-shaping assumptions used by downstream stages

The goal is invocation-path replacement, not accidental business-logic drift.

### Guardrail 5 — Do not optimize batching in the first pass
First pass should prioritize deterministic replacement over throughput optimization.

Recommended first pass:
- one article per API call
- preserve ordering
- preserve current limit behavior

Only consider batching after correctness and output compatibility are validated.

---

## 13. Recommendation

### Recommended next move
Implement this as a **bounded Phase A migration only**.

Do not combine it with:
- Phase B migration
- delivery changes
- orchestrator restructuring
- config redesign

### Best sequence
0. audit current Phase A behavior + freeze schema
1. add direct-API helper
2. swap Phase A internals to use it
3. add tests
4. run controlled validation
5. update implementation plan immediately after milestone completion

---

## 14. Bottom line

For Phase A scoring, direct DeepSeek API usage is the right architectural direction.

It better matches the true shape of the task:
- fixed input
- fixed output
- deterministic pipeline stage

This should reduce framework overhead and make RSS-Brew more like an actual application pipeline and less like a conversation-mediated workflow.
