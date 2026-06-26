# RSS-Brew Scoring V2 — Implementation Plan (Revised)

Date: 2026-03-12
Owner: Watson
Status: revised after Chongzhi + Pinker review

## Objective

Replace the current fragile single-score pipeline with a more robust 3-layer system:

1. **Rule-based filtering and scoring**
2. **Model judgment scoring**
3. **Ranking and distribution control**

Target outcomes:
- improve score quality and explainability
- prevent score inflation
- keep digest output balanced (`Deep Set` vs `Other New Articles`)
- reduce model cost/runtime by filtering obvious low-value content before model scoring
- preserve compatibility with the current RSS-Brew runner during rollout

---

## Current problems

### 1. Score inflation
Observed on 2026-03-12:
- total scored: 74
- score 4: 25
- score 5: 25
- result: 50 items qualified for deep handling

### 2. Poor distribution control
Historically, `score >= 4` flowed into `Deep Set`, leaving too few items in `Other New Articles`.

### 3. Low explainability
Current output is just:
- one integer score
- one short reason

This is insufficient for debugging, calibration, and editorial review.

### 4. Cost and latency inefficiency
Many low-value or malformed items still go through model scoring.

### 5. Selection ownership ambiguity
Today, `phase_b_analyze.pick_deep_set()` still performs selection internally. This must be changed so only one stage owns distribution decisions.

---

## V2 design principles

1. **Compatibility first**: keep current contracts stable during rollout.
2. **Single owner per decision**: only one stage decides `Deep Set` / `Other` membership.
3. **Rule before model**: do not spend model tokens on obvious junk.
4. **Model score is a modifier, not a kingmaker**.
5. **Distribution is editorial, not threshold-derived**.

---

## V2 architecture

## Layer 1 — Rule-based filtering and scoring

### Purpose
Cheap, deterministic filtering before model usage.

### 1A. Hard filters (do not enter model scoring)
Reject item if any severe condition holds:
- extraction is obviously corrupted /乱码 / malformed body
- teaser-only content with extremely short body/summary
- obvious promo / sponsored / registration / CTA page
- duplicate URL or strong duplicate-title cluster
- thin product/tool announcement with no scenario / no user need / no business relevance

### 1B. Rule-based scoring (programmatic)
Compute `rule_score` from deterministic signals.

#### Positive candidates
- text length > 2000 chars: `+1`
- text length > 5000 chars: additional `+1`
- clear multi-case roundup / list / 5+ examples: `+1`
- explicit balanced structure / opposing views markers: `+1`
- high Richard-domain keyword relevance (VC / AI / China / startup / strategy / market structure): `+1`

#### Negative candidates
- promo / sponsored / event sales / “register now”: `-1`
- heavy CTA / end-of-article selling intent: `-3`
- teaser-only / low information density: `-1`
- corrupted extraction / very low text quality: `-2`
- tool/product mention without pain point / use case / business framing: `-1`

### 1C. Rule output schema
Each surviving article gets:

```json
{
  "rule_score": 1,
  "rule_plus_tags": ["length_gt_2000", "domain_relevant"],
  "rule_minus_tags": ["promo_like"],
  "rule_reject": false,
  "rule_reject_reason": ""
}
```

### 1D. Over-filtering fallback
To avoid over-filtering:
- if `rule_pass_count < floor_count`, auto-relax selected filters
- recommended `floor_count = 12`
- breaking-news override must be config-based (source + title regex), not prompt-only

---

## Layer 2 — Model judgment scoring

### Purpose
Use model reasoning only on items that passed Layer 1.

### Core rule
The model should not emit only one vague scalar. It must output:
- matched positive tags
- matched negative tags
- short evidence for each major claim
- `model_score`
- `confidence`
- legacy-compatible `score`

### Scoring families
Adopt Richard's content-value system, adapted for RSS-Brew.

#### Positive model tags
- global_important_person_first_hand_interview: `+1`
- china_important_person_first_hand_interview: `+1`
- breaking_news_incremental_interpretation: `+1`
- insightful_explainer: `+1`
- multi_case_roundup: `+1`
- balanced_views_or_cases: `+1`
- substantial_first_hand_practice: `+1`
- exclusive_insider_reveal_signal: `+1`
- decision_usefulness: `+1`

#### Negative model tags
- one_sided_pr_or_agitprop: `-1`
- overly_technical_without_user_or_business_context: `-1`
- insufficient_supporting_data_vs_claims: `-1`
- product_intro_without_use_case_or_need: `-1`
- article_serves_end_of_piece_sale: `-3`

### Subjective-tag control rules
To reduce drift:
- `important_person` tags use configurable name/keyword lists; unknown => no score
- `exclusive/insider/reveal` prefer keyword + evidence, not free intuition
- `humorous/commentary style` is excluded from V2 core scoring in V1 rollout; it may be added later as a secondary editorial bonus, not a primary value signal

### Model score range
To avoid inflation:
- `model_score` is constrained to **-3 to +3**
- it acts as a modifier, not an independent large score ladder

### Legacy compatibility requirement
During rollout, every article must still carry:
- `score` (legacy integer field)
- `score_reason`

Proposed mapping during rollout:
- keep `score` as a compressed legacy value derived from `final_score` or controlled calibration
- add V2 fields alongside it

### Model output schema

```json
{
  "model_score": 2,
  "confidence": "high",
  "plus_tags": [
    {
      "tag": "breaking_news_incremental_interpretation",
      "score": 1,
      "evidence": "Explains the implication of the event rather than restating the headline."
    },
    {
      "tag": "insightful_explainer",
      "score": 1,
      "evidence": "Provides structural reasoning and not just chronology."
    }
  ],
  "minus_tags": [
    {
      "tag": "insufficient_supporting_data_vs_claims",
      "score": -1,
      "evidence": "Claims broad importance but uses only one weak example."
    }
  ],
  "score_reason": "Useful explainer with incremental insight, but evidence depth is moderate.",
  "score": 4
}
```

---

## Layer 3 — Ranking and distribution control

### Purpose
Editorial control after scoring. Do not rely on threshold-only behavior.

### Final score

```text
final_score = rule_score + model_score
```

Additional ranking modifiers may be applied without changing stored score:
- recency bonus
- source diversity bonus
- topic diversity bonus
- confidence penalty

### Confidence penalty policy (explicit)
- `high`: no penalty
- `medium`: no automatic penalty
- `low`: cannot enter top 3; if otherwise selected, it may appear in `Other` but not in top-3 `Deep Set`

### Bucket policy
Do not map `score >= X` directly to Deep Set.
Instead:
1. sort by `final_score`
2. apply source/topic/confidence guardrails
3. allocate into output buckets

### Proposed bucket targets
- `Deep Set`: top 5
- `Other New Articles`: next 10-15
- remainder: archive/index only, not shown in digest main body

### Guardrails
- `Other New Articles` minimum retained: 5
- max items from one source in main digest: 3
- max items from one topic in `Deep Set`: 2 *(deferred by default in current V2 runtime)*
- low-confidence items cannot enter top 3

### Topic/source cap note
Current pipeline has `category`, not a reliable topic taxonomy. For V1 rollout:
- apply **source caps first** (deterministic)
- topic caps remain optional until topic normalization is stable enough
- current V2 default keeps deep topic cap **disabled** unless explicitly opted in (`--enforce-deep-topic-cap`), and only when normalized topic keys are available

---

## Ownership changes (must-have)

### Single owner rule
`Deep Set` / `Other` selection must happen in **one place only**.

### New ownership
- `phase_rank_distribute` owns:
  - final ranking
  - deep selection
  - other selection
- `phase_b_analyze` becomes:
  - analyze provided Deep Set only
  - no internal `pick_deep_set()` selection logic
- `digest_writer` must read explicit `deep-set.json` and `other-set.json`
  - it must **stop deriving** `others = scored - deep_urls`

---

## Pipeline behavior changes

## Current
core_pipeline -> phase_a_score -> phase_b_analyze -> digest_writer

## Proposed V2 (feature-flagged)
core_pipeline
-> phase_rule_filter_score
-> phase_model_score
-> phase_rank_distribute
-> phase_b_analyze (Deep Set only)
-> digest_writer

### Feature flag requirement
V2 must ship behind a feature flag:
- CLI flag: `--scoring-v2`
- or env flag: `RSS_BREW_SCORING_V2=1`

Current path remains available as rollback path.

---

## Data artifacts

### New intermediate files
- `rule-filtered-articles.json`
- `model-scored-articles.json`
- `ranked-articles.json`
- `distribution.json`
- `other-set.json`

### Existing artifacts retained
- `new-articles.json`
- `scored-articles.json` (kept for compatibility during rollout)
- `deep-set.json`
- `daily-digest-YYYY-MM-DD.md`

---

## Rollout strategy

## Stage 0 — No-contract-break version
- keep current pipeline working
- add V2 fields alongside legacy score fields
- no downstream consumer breakage allowed

## Stage 1 — Rule filter/scorer
Create `phase_rule_filter_score.py`
Responsibilities:
- reject obvious low-value inputs
- add rule tags and rule score
- emit filtered payload for model stage

## Stage 2 — Structured model scoring
Refactor current Phase A into `phase_model_score.py`
Responsibilities:
- consume rule-filtered inputs
- emit structured tags/evidence/confidence/model_score
- still preserve legacy `score` / `score_reason`

## Stage 3 — Rank/distribute
Create `phase_rank_distribute.py`
Responsibilities:
- calculate final score
- sort items
- apply source/confidence guardrails
- output `deep-set.json` and `other-set.json`

## Stage 4 — Narrow Phase B scope
Refactor `phase_b_analyze.py` to consume only the selected Deep Set list.
This should materially reduce GLM runtime.

## Stage 5 — Update digest writer
Refactor `digest_writer.py` to read:
- `deep-set.json`
- `other-set.json`
rather than inferring `Other = scored - deep`

## Stage 6 — Calibrate and tighten
Only after several stable runs:
- refine confidence penalties
- add optional topic caps
- consider editorial secondary bonuses (e.g. commentary/readability)

---

## Observability

Add stats to manifest/logs:
- filtered_out_count
- rule_pass_count
- model_scored_count
- deep_set_selected_count
- other_selected_count
- score_distribution
- per-stage durations
- feature-flag state (`scoring_v2: true/false`)

These should be persisted in the run-record manifest, not only ad hoc files.

---

## Recommended first-cut thresholds

### Hard filter examples
- reject if `len(summary) < 80` and `len(text) < 400`
- reject if corruption heuristic exceeds threshold
- reject if promo keyword density is high and domain relevance low

### Distribution defaults
- deep_set_target = 5
- other_target = 12
- main_digest_source_cap = 3
- top3_low_confidence_block = true

### Fallback defaults
- minimum rule-pass floor = 12
- breaking-news override allowlist enabled

---

## Risks

### 1. Over-filtering
Aggressive rule filtering may wrongly reject short but important breaking news.
Mitigation:
- explicit breaking-news override config
- minimum pass floor with auto-relax behavior

### 2. Tag drift
Model may still over-assign subjective tags.
Mitigation:
- require evidence strings
- use keyword lists for important-person / insider tags
- exclude style-only tags from core V1 scoring

### 3. Complexity growth
Pipeline gains more stages and artifacts.
Mitigation:
- keep each stage single-purpose
- add explicit artifacts and logs for debugging
- ship behind feature flag

### 4. Contract breakage
Downstream consumers still expect current files/fields.
Mitigation:
- retain legacy `score` and `scored-articles.json` during rollout
- add regression tests before cutover

---

## Test plan (required before cutover)

### Contract tests
- `run_pipeline_v2.py` still produces expected top-level artifacts
- legacy mode remains untouched when feature flag is off

### Regression fixtures
Validate on saved real runs:
- Deep Set count ~= target
- Other count populated
- source cap respected
- low-confidence items excluded from top 3
- rollback path still works

### Runtime comparison
Compare V1 vs V2 on:
- phase durations
- number of model-scored items
- Phase B runtime
- final digest shape

---

## Success criteria

A good V2 run should show:
- clear drop in high-score inflation
- stable digest shape day-to-day
- Deep Set remains curated (around 5)
- Other remains visibly populated (around 10-15)
- shorter Phase B runtime than current production mode
- better explainability for why articles were selected
- no breakage in existing runner/publish path during rollout

---

## Immediate recommendation

Implement V2 in this order:
1. rule filter + rule score
2. structured model scoring while preserving legacy fields
3. rank/distribute with explicit Deep/Other ownership
4. refactor Phase B to analyze provided Deep Set only
5. refactor digest_writer to consume explicit Other list
6. calibrate confidence and subjective-tag behavior on real runs
