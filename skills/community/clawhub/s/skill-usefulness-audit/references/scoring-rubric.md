# Scoring Rubric

Score each skill with one local 10-point score, one final score, and side signals.

## Contents

- Core Outputs
- Usage Score
- Uniqueness Score
- Impact Score
- Confidence Score
- Quality Penalty
- Community Prior Score
- Static Risk Level
- Verdict Bands
- Action Rules

## Core Outputs

- `local_score = usage_score + uniqueness_score + impact_score`
- `quality_penalty`: `0.0-2.5`
- `quality_penalty_uncapped`: raw quality burden before the cap
- `final_score = clamp(local_score - quality_penalty, 0.0, 10.0)`
- `usage_score`: `0.0-3.0`
- `uniqueness_score`: `0.0-3.0`
- `impact_score`: `0.0-4.0`
- `confidence_score`: `0.0-1.0`
- `community_prior_score`: `0.0-1.0`
- `risk_level` / `static_risk_level`: `none / low / medium / high`

Keep `community_prior_score` and static risk fields separate from `local_score`.
Use quality burden, community prior, and static risk hints to shape review priority and final action.

## 1. Usage Score (`0.0-3.0`)

Prefer direct host usage logs.
Use transcript mentions only as weaker fallback evidence.

### Input Fields

- `calls`
- `recent_30d_calls`
- `recent_90d_calls`
- `last_used_at`
- `active_days`

History fallback fields:

- `history_mentions`
- `suspected_invocations`

Transcript mentions are weak evidence only. They may influence the usage score through the history evidence weight, but they must not be reported as direct `calls`.
- `usage_source`
- `evidence_weight`
- `executions`
- `script_failures`
- `repair_turns`
- `reference_loads`
- `false_triggers`

### Base Usage Strength

- When `recent_30d_calls` exists:
  - `0.0`: `0`
  - `1.0`: `1-2`
  - `2.0`: `3-7`
  - `3.0`: `8+`
- When only `recent_90d_calls` exists:
  - `0.0`: `0`
  - `0.75`: `1-2`
  - `1.5`: `3-9`
  - `2.5`: `10+`
- When only total `calls` exists:
  - `0.0`: `0`
  - `1.0`: `1-2`
  - `2.0`: `3-9`
  - `3.0`: `10+`

### Recency Adjustments

- add `0.5` when `last_used_at <= 7 days`
- add `0.25` when `last_used_at <= 30 days`
- subtract `0.5` when `last_used_at > 180 days`
- add `0.25` when `active_days >= 10`
- add `0.10` when `active_days >= 3`

### Evidence Weight

- `1.00`: direct usage file
- `0.45`: transcript-history fallback based on `suspected_invocations`
- `0.00`: missing usage evidence

Clamp the final usage score to `0.0-3.0`.

## 2. Uniqueness Score (`0.0-3.0`)

Measure the highest functional-overlap similarity against any other installed skill.
Use description, headings, and resource names as the comparison surface.

Buckets:

- `0.0`: highest overlap `>= 0.85`
- `1.0`: highest overlap `0.65-0.84`
- `2.0`: highest overlap `0.40-0.64`
- `3.0`: highest overlap `< 0.40`

## 3. Impact Score (`0.0-4.0`)

### General skills

Use ablation on historical conversations.
Compute:

- `consistency_rate`: skill-on and skill-off produce materially equivalent outcomes
- `better_rate`: skill-on clearly improves the result
- `worse_rate`: skill-on clearly harms the result

Base score from consistency:

- `0.0`: `consistency_rate >= 0.85`
- `1.0`: `0.70-0.84`
- `2.0`: `0.55-0.69`
- `3.0`: `0.35-0.54`
- `4.0`: `< 0.35`

Adjustments:

- add `1.0` when `better_rate - worse_rate >= 0.30`
- subtract `1.0` when `worse_rate > better_rate`
- clamp the final impact score to `0.0-4.0`

When ablation is missing, use low-evidence score `1.0` for zero-call skills.
For skills with direct usage evidence but no ablation yet, keep temporary neutral score `2.0` and lower confidence.

### API and tool skills

Skip history ablation.
Use protected-capability scoring instead:

- start at `2.0`
- add `1.0` when the skill ships executable scripts or hard capability resources
- add `0.5` when highest overlap `< 0.35`
- add `0.5` when calls `>= 3`
- subtract `1.0` when highest overlap `>= 0.75`
- subtract `0.5` when calls are `0`
- clamp the final impact score to `0.0-4.0`

## 4. Confidence Score (`0.0-1.0`)

Confidence describes evidence quality, not usefulness.

Add:

- `0.35` for direct usage files
- `0.15` for history fallback
- `0.20` when recent usage fields exist
- `0.10` when only total direct calls exist
- `0.25` for protected `api/tool` classification
- `0.25` for `general` skills with `>= 5` ablation cases
- `0.15` for `general` skills with `1-4` ablation cases
- `0.10` when overlap comparison has peers
- `0.05` when only one skill exists in scope
- `0.10` when community metadata exists

Clamp the final confidence score to `0.0-1.0`.

## 5. Quality Penalty (`0.0-2.5`)

Quality penalty captures the cost of keeping a skill even when it has some utility.
It is a deduction from `local_score`, not a risk flag.

### Runtime burden

Use direct usage logs when available:

- add `0.45` when `calls >= 8` and `executions / calls < 0.25`
- add `0.35` when `false_triggers >= 3` or `false_triggers / calls >= 0.25`
- add `0.40` when `calls >= 5`, `consistency_rate >= 0.85`, and `better_rate <= 0.10`
- add `0.30` when `reference_loads >= 10` and `reference_loads / calls >= 3.0`
- add `0.45` when script failures are frequent
- add `0.20` when script failures are occasional
- add `0.30` when `repair_turns >= 3`

### Static bundle burden

Scan installed skill files:

- add `0.20-0.40` for large `SKILL.md` bodies
- add `0.10-0.25` for frontmatter descriptions that are too long for concise routing
- add `0.25` for broad trigger language in the frontmatter description
- add `0.20-0.30` when reference files are not directly disclosed from `SKILL.md`
- add `0.25-0.50` for large reference sets or heavy reference text
- add `0.10-0.20` when long reference files have no visible table of contents
- add `0.20` when resource filenames are too generic for selective loading
- add `0.25-0.50` for large assets directories
- add `0.60` for bundled files that look private or environment-specific
- add `0.30` for executable assets
- add `0.10-0.20` when script count suggests over-bundling
- add `0.25-0.40` for scripts with placeholders, local absolute paths, or maintenance smells
- add `0.50` for Python script syntax errors

Clamp the combined penalty to `0.0-2.5`.
Emit `quality_flags`, `quality_evidence`, `resource_metrics`, `quality_penalty_uncapped`, and `score_breakdown.quality`.

## 6. Community Prior Score (`0.0-1.0`)

Treat community data as external prior, not a local verdict.

Weighted components:

- `0.30`: normalized rating
- `0.20`: current installs or downloads
- `0.10`: all-time installs
- `0.15`: trending metric
- `0.10`: stars
- `0.05`: comments
- `0.10`: maintenance freshness from `last_updated`

Use it to rank review priority and benchmark replacements.

Emit `community_breakdown` in JSON so users can see which registry signals contributed.

## 7. Static Risk Level

Run static scans against runnable scripts and resource files.
This is lint-style evidence only. It cannot prove a skill is safe, because indirection, dynamic imports, encoded payloads, aliases, or external downloads can evade simple pattern matching.

Typical flags:

- `curl-pipe-shell`
- `dynamic-exec`
- `protected-path-access`
- `persistence-hook`
- `external-post`
- `shell-exec`
- `network-download`
- `base64-payload`

Static risk levels:

- `none`: `0.0`
- `low`: `0.0 < score < 2.0`
- `medium`: `2.0-3.9`
- `high`: `4.0+`

## Verdict Bands

Use `final_score` for verdict bands.

- `8.0-10.0`: keep
- `6.0-7.9`: keep, narrow when overlap stays high
- `4.5-5.9`: review
- `3.0-4.4`: merge or delete candidate
- `0.0-2.9`: strong delete candidate

## Action Rules

- `high static risk`: `quarantine-review`
- `medium static risk + strong final score`: `keep-review-risk`
- `high quality burden + strong final score`: `keep-review-burden`
- `high quality burden + mid final score`: `review-burden`
- `low confidence + weak final score`: `observe-30d`
- `low final score + high overlap`: `merge-delete`
- `very low final score`: `delete`
- `low final score + strong community prior`: `review-vs-community`

Community data shapes review order.
Static risk level shapes manual review priority.
Quality burden turns "useful but expensive" skills into review items.

`delete`, `merge-delete`, and `quarantine-review` are report recommendations only. They are never permission for automatic deletion, isolation, or disabling without human review.
