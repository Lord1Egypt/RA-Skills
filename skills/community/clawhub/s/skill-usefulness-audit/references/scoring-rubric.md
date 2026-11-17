# Scoring Rubric

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
- `static_quality_penalty`: `0.0-1.4`
- `final_score = clamp(local_score - quality_penalty, 0.0, 10.0)`
- `risk_level` / `static_risk_level`: `none / low / medium / high`

## 1. Usage Score (`0.0-3.0`)

Prefer direct host usage logs.
Use transcript mentions only as weaker fallback evidence.

### Input Fields

- Direct usage: `calls`, `recent_30d_calls`, `recent_90d_calls`, `last_used_at`, and `active_days`.
- History fallback: `history_mentions` and `suspected_invocations`. These are weak evidence weighted through history and must not be reported as direct `calls`.
- Evidence and runtime burden: `usage_source`, `evidence_weight`, `executions`, `script_failures`, `repair_turns`, `reference_loads`, and `false_triggers`.

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

## 2. Uniqueness Score (`0.0-3.0`)

Measure the highest functional-overlap similarity against any other installed skill using descriptions, headings, and resource names.

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

When ablation is missing, use low-evidence score `1.0` for zero-call skills.
For skills with direct usage evidence but no ablation yet, keep temporary neutral score `2.0` and lower confidence.

### API and tool skills

Skip history ablation.
Use protected-capability scoring instead:

- start at `2.0`
- add `1.0` when the skill ships executable scripts or reference files
- add `0.5` when highest overlap `< 0.35`
- add `0.5` when calls `>= 3`
- subtract `1.0` when highest overlap `>= 0.75`
- subtract `0.5` when calls are `0`

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
- `0.10` when more than one skill is in scope
- `0.05` when only one skill exists in scope
- `0.10` when community metadata exists

## 5. Quality Penalty (`0.0-2.5`)

Quality penalty captures the cost of keeping a skill and is deducted from `local_score`; it is not a risk flag.

### Runtime burden

Use direct usage logs when available:

- `overtrigger-low-execution`: `0.45` when `calls >= 8` and `executions / calls < 0.25`
- `overtrigger-misfire`: `0.35` when `calls >= 5` and (`false_triggers >= 3` or `false_triggers / calls >= 0.25`)
- `overtrigger-no-impact`: `0.40` when `calls >= 5`, `consistency_rate >= 0.85`, and `better_rate <= 0.10`
- `reference-overload`: `0.30` when `reference_loads >= 10` and `reference_loads / calls >= 3.0`
- `script-failure-burden`: `0.45` when `script_failures >= 3` or the failure rate against executions (or calls) reaches `0.30`; `0.20` below that
- `agent-repair-burden`: `0.30` when `repair_turns >= 3`

### Readiness burden

- `missing-required-env`: `0.90` when declared required environment variables are not configured in the current audit process

### Catalog burden

- `near-duplicate-instructions`: `0.10` when the instruction fingerprint closely matches another installed skill

### Static bundle burden

Scan installed skill files:

- `empty-skill-contract`: `0.80` when the skill has no meaningful runtime contract beyond minimal or missing metadata
- `prompt-bloat`: `0.40` when `SKILL.md` body is at least `5000` context units
- `prompt-bloat`: `0.20` when `SKILL.md` body is at least `2500` context units
- `broad-trigger-surface`: `0.25` for at least two broad trigger matches, or one match with description at `30+` context units
- `description-bloat`: `0.25` when the frontmatter description is at least `120` context units
- `description-bloat`: `0.10` when the frontmatter description is at least `60` context units
- `reference-disclosure-gap`: `0.30` when at least 3 reference files exist and none are directly discoverable from `SKILL.md`
- `reference-disclosure-gap`: `0.10` when 1-2 reference files exist and none are directly discoverable from `SKILL.md`
- `reference-disclosure-gap`: `0.20` when at least 8 reference files exist and fewer than 30% are directly linked from `SKILL.md`
- `reference-link-broken`: `0.25` when `SKILL.md` points to missing reference files
- `reference-bloat`: `0.50` when references are at least 50 files or 50000 context units
- `reference-bloat`: `0.25` when references are at least 20 files or 15000 context units
- `long-reference-without-toc`: `0.20` when at least 3 reference files over `100` lines lack a visible table of contents
- `long-reference-without-toc`: `0.10` when 1-2 such files lack one
- `reference-content-pollution`: `0.35` when references include advertising, upsells, unrelated text, or other-tool/skill promotion
- `asset-bloat`: `0.50` when assets are at least 200 files or 100 MB
- `asset-bloat`: `0.25` when assets are at least 50 files or 25 MB
- `vague-resource-names`: `0.20` when at least 5 scripts, references, or assets use generic filenames
- `private-bundle-artifact`: `0.60` when bundled filenames look private or environment-specific
- `private-content-artifact`: `0.60` when bundled content looks like credentials or keys
- `executable-asset`: `0.30` when assets contain executable binaries or installers
- `script-count-bloat`: `0.20` when the bundle has at least 40 scripts
- `script-count-bloat`: `0.10` when the bundle has at least 20 scripts
- `script-maintenance-smell`: `0.40` when at least 8 scripts contain placeholders, local absolute paths, or maintenance smells
- `script-maintenance-smell`: `0.25` when 1-7 scripts contain placeholders, local absolute paths, or maintenance smells
- `script-syntax-error`: `0.50` when Python scripts contain syntax errors
- `script-import-error`: `0.50` when Python scripts import modules missing from the local environment or bundle

Clamp `static_quality_penalty` to `0.0-1.4`, then clamp the combined `quality_penalty` to `0.0-2.5`.

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

Normalization: rating divides by `5.0`; volume signals use `log1p` with saturation `5000` (current), `20000` (all-time), `250` (trending, stars), and `100` (comments); maintenance scores `1.0/0.7/0.4/0.1` at `<=180/<=365/<=730/>730` days.

## 7. Static Risk Level

Run static scans against runnable scripts and resource files.
Only fenced code blocks in `SKILL.md` and directly linked Markdown references are scanned as commands; prose outside fences and unlinked references are not command-scanned.
Credential-like content checks still cover `SKILL.md`, scripts, assets, references, and root text files without echoing matched values.
This is lint-style evidence only; it cannot prove a skill is safe.

Typical flags: `curl-pipe-shell`, `dynamic-exec`, `protected-path-access`, `persistence-hook`, `external-post`, `shell-exec`, `network-download`, and `base64-payload`.

Static risk levels:

- `none`: `0.0`
- `low`: `0.0 < score < 2.0`
- `medium`: `2.0-3.9`
- `high`: `4.0+`

If static quality finds `private-content-artifact`, that evidence is promoted to `high` risk so credential-like bundled content receives `quarantine-review`.

## Health Cap

Some quality findings cap the final score even when usage or protected-capability signals are strong:

- `script-syntax-error`: final score cap `4.0`
- `empty-skill-contract`: final score cap `5.5`
- `script-import-error`: final score cap `5.5`
- `script-failure-burden`: final score cap `4.0` when the penalty is at least `0.45`

## Verdict Bands

Use `final_score` for verdict bands.

- confidence `< 0.55` and `final_score < 4.5`: `insufficient-evidence`
- `8.0-10.0`: `keep`
- `6.0-7.9`: `keep-narrow`
- `4.5-5.9`: `review`
- `3.0-4.4`: `merge-delete`
- `0.0-2.9`: `delete`

## Action Rules

Evaluate top to bottom; the first matching rule wins.

| Condition | Action |
| --- | --- |
| system source, high risk / otherwise | `review-system` / `keep-system` |
| high risk | `quarantine-review` |
| medium risk and score `>= 6.0` | `keep-review-risk` |
| quality penalty `>= 1.2` and score `>= 6.0` / `>= 4.5` | `keep-review-burden` / `review-burden` |
| score `>= 8.0` / `>= 6.0` | `keep` / `keep-narrow` |
| remaining medium risk | `review-risk` |
| confidence `< 0.55` | `observe-30d` |
| score `>= 4.5`: overlap `>= 0.65` / community prior `>= 0.6` / otherwise | `merge-or-review` / `review-vs-community` / `review` |
| API/tool skill: zero calls and overlap `>= 0.75` / community prior `>= 0.6` / otherwise | `merge-delete` / `review-vs-community` / `merge-or-review` |
| community prior `>= 0.6` | `review-vs-community` |
| score `< 3.0` | `delete` |
| otherwise, including overlap `>= 0.65` with calls `<= 1` | `merge-delete` |
