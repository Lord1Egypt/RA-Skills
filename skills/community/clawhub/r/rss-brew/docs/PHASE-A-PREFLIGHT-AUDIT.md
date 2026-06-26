# RSS-Brew Phase A Preflight Audit

**Date:** 2026-03-09  
**Status:** Completed  
**Scope:** Audit current `scripts/phase_a_score.py` behavior before any direct DeepSeek API migration.

---

## 1. Current Phase A role

Current Phase A file:

```text
scripts/phase_a_score.py
```

Current responsibility:
- read `new-articles.json`
- score each article
- write `scored-articles.json`

Current call site:
- `scripts/run_pipeline_v2.py`

Current downstream consumer:
- `scripts/phase_b_analyze.py`

---

## 2. Current prompt / scoring behavior

### System prompt
Current system prompt is very small and strict:

- return strict JSON only
- output shape:
  - `score: int`
  - `score_reason: str`
- score range: `0..5`
- score is based on five binary dimensions:
  - Value & Insight
  - Relevance
  - Depth & Data
  - Authority
  - Objectivity
- `score_reason` should be one short sentence

### User prompt fields sent to the model
For each article, the prompt currently includes:
- title
- source
- published
- url
- summary or truncated text body

### Text selection behavior
Current Phase A chooses article text like this:
1. prefer `summary`
2. if no summary, use first 800 chars of `text`

This is important and should be preserved unless intentionally changed.

---

## 3. Current model invocation pattern

Current invocation inside `score_one(...)`:
- `chat_completion(model_alias, SYSTEM, prompt)`

Operational default:
- `--model CHEAP`

So today Phase A is already structured as a single-article scoring call with:
- fixed system prompt
- fixed user prompt shape
- simple JSON parse

This confirms that Phase A is a good candidate for direct API migration.

---

## 4. Current parse / validation behavior

### Parsing
Current code expects model output to be JSON.

Primary path:
- `json.loads(content)`

Fallback path:
- if JSON decoding fails, scan for first `{` and last `}` and try parsing substring

### Validation
Current validation is intentionally light:
- `score` is passed through `clamp_score(...)`
- any invalid/non-int score becomes `0`
- `score_reason` is stringified and stripped
- if missing/empty, fallback to:
  - `"Scored by Phase-A rubric."`

### Important implication
Current Phase A is tolerant of slightly messy model output.

A direct API migration should preserve equivalent robustness unless intentionally tightened.

---

## 5. Current mock behavior

Mock mode is not random.

It uses keyword-signal counting against:
- `ai`
- `startup`
- `vc`
- `fund`
- `data`
- `market`

Then:
- converts signal count into score via clamp
- writes fixed reason:
  - `Mock scoring based on keyword signal.`

This means mock mode has a deterministic role in dry-runs/tests and should not be broken casually.

---

## 6. Current input contract

Current input file shape (from `new-articles.json`):
- top-level object
- key: `generated_at`
- key: `article_count`
- key: `articles`

Each article currently arrives with fields such as:
- `source`
- `source_url`
- `title`
- `url`
- `published`
- `summary`
- `text`

Phase A currently assumes at least:
- `title`
- `source`
- `published`
- `url`
- `summary` or `text`

But it is tolerant of missing values by defaulting to empty strings.

---

## 7. Current output contract (schema freeze candidate)

Current top-level `scored-articles.json` shape:
- `generated_at`
- `article_count`
- `model`
- `articles`

Per article, current output preserves the original article fields and adds:
- `score`
- `score_reason`

This is the most important migration constraint.

### Current schema freeze recommendation
For the first direct-API migration pass, preserve exactly:
- original article payload as-is
- plus `score`
- plus `score_reason`

Do not add or rename fields in V1 of the migration.

---

## 8. Downstream assumptions

Current downstream Phase B (`scripts/phase_b_analyze.py`) uses:
- `score`
- original article fields like title/source/url/published/summary/text

Specific Phase B dependency:
- deep-set selection is based on `int(article.get("score", 0))`
- if no article has score >= 4, Phase B falls back to top 3 by score

### Important implication
Even subtle score drift can change:
- which articles enter deep analysis
- whether fallback mode triggers
- final digest composition

So Phase A migration is not just a local performance change; it can materially shift downstream output.

---

## 9. Migration implications

### Safe to preserve exactly
- one article in -> one scored article out
- top-level file shape
- `score` and `score_reason` fields
- summary-first / text-fallback input selection
- limit behavior
- article ordering

### Areas that need explicit care
- JSON parse robustness
- score drift due to model change
- prompt parity vs current rubric wording
- runtime/cost impact of `deepseek-reasoner`

---

## 10. Recommendations before implementation

### Recommendation 1 — Freeze schema now
Use current `scored-articles.json` shape as the migration contract.

### Recommendation 2 — Preserve single-article call shape first
Do not batch in the first pass.

### Recommendation 3 — Keep parse fallback behavior
Direct API migration should preserve robust JSON extraction behavior or intentionally replace it with something stricter plus bounded retry.

### Recommendation 4 — Measure score drift on sample set
Before replacing production scoring fully, compare old and new outputs on a fixed article sample.

### Recommendation 5 — Keep mock mode working
Tests and dry-runs depend on deterministic mock scoring behavior.

---

## 11. Bottom line

Phase A is structurally a strong candidate for direct DeepSeek API migration.

However, the migration must preserve three things:
1. output schema
2. prompt/rubric intent
3. downstream score semantics

The highest practical migration risk is not parsing. It is **score drift affecting Phase B selection and final digest composition**.
