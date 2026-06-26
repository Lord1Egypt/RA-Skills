# P02 Match installed skills to JD

## Objective

Run **two-stage** matching: **P02a** broad recall into a shortlist, then **P02b** rubric precision on that shortlist only. Decide: auto-delegate, confirm with user, or recruit.

Machine-readable output **must** conform to [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json).

## Inputs

- `jd`: JSON from P01 (including optional `search_queries`, `competency_tags`).
- `candidates`: for each installed skill, at minimum:
  - `id`, `name`, frontmatter `description`
  - **Excerpts**: short quotes from `SKILL.md` body (triggers, workflows, boundaries)—not description alone
  - `registry_status` from `.skill-hr/registry.json` when present, or from benchmark `skill_catalog[].registry_status`: `active` \| `on_probation` \| `terminated` \| `frozen`
  - Optional registry stats: `tasks_success`, `tasks_total`, `last_used_at`, per-skill `notes`
- `matching_config`: `delegate_min_score`, `confirm_band_min` (defaults **75** / **60**).

## Phase P02a — Broad recall (shortlist)

**Goal:** Reduce the full pool to **≤ 12** skills (target **8–10**) without deep scoring.

1. **Filter pool**: omit `terminated`, `frozen`. **Exclude `skill-hr`** unless the JD is explicitly about skill operations (install, registry, match, retire skills)—see [`../matching-lexicon.md`](../matching-lexicon.md) meta routing.
2. For each remaining skill, gather **signals** (cheap):
   - Overlap between JD (`mission_statement`, `must_have_competencies`, `deliverables`, `search_queries`, `competency_tags`) and skill `description` + **body excerpts**
   - Lexicon hints from [`../matching-lexicon.md`](../matching-lexicon.md) (artifact family, integration surface, adjacency warnings)
3. **Include hard negatives** when two skills share tokens: both stay on the shortlist if plausible until P02b disambiguates (do not drop the correct skill to hit the cap—if unsure, widen to 12).
4. Emit **`recall_shortlist`**: ordered list of `skill_id` (best recall first). Every `skill_id` in P02b must appear here.

## Phase P02b — Precision rubric (shortlist only)

For each `skill_id` in `recall_shortlist` only:

1. Score **0–100** total using [`../03-matching-rubric.md`](../03-matching-rubric.md).
2. Emit **required dimension sub-scores** (each 0..max for that dimension):

| Dimension key | Max | Maps to rubric |
|---------------|-----|----------------|
| `outcome_fit` | 40 | Outcome fit |
| `competency_coverage` | 30 | Competency coverage |
| `tool_stack_fit` | 15 | Tool / stack fit |
| `quality_safety` | 10 | Quality / safety posture |
| `freshness_trust` | 5 | Freshness / trust |

3. **`competency_coverage_matrix`**: for **each** string in `jd.must_have_competencies`, one row:

   - `competency` (echo JD line)
   - `coverage`: `covered` \| `partial` \| `missing`
   - `evidence`: one short **quote or faithful paraphrase** tied to skill text; use `""` only if `missing`

4. **`hard_negative_explanations`** (when shortlist has ≥2 plausible skills): list objects `{ "skill_id", "excluded_because" }` for **runner-up** skills you reject vs `best`—cite scope, wrong artifact, missing tool, or registry `notes` conflict per [`../03-matching-rubric.md`](../03-matching-rubric.md).

5. **`evidence`**: 2–5 bullets (strings) supporting the total score (may reference sub-scores).

6. **`gaps`**: JD competencies or tools **still** weak or missing for this skill.

7. **`confidence`**: `high` \| `medium` \| `low` from evidence strength (stale registry / thin excerpts → cap at `medium` for borderline scores).

8. **Rank** all P02b rows by **total `score`** descending; apply **tie-break** from `03-matching-rubric.md` using registry stats when available.

## Output schema (JSON)

**Do not invent fields** outside the JSON Schema. Top-level shape:

- `recall_shortlist`: string[]
- `candidates`: array of precision objects (only shortlist skills), each with `skill_id`, `skill_name`, `score`, `subscores`, `competency_coverage_matrix`, `evidence`, `gaps`, `confidence`, and optional `hard_negative_explanations` (may be empty array)
- `best`: `{ "skill_id", "score" }` — highest after tie-break
- `decision`: `delegate` \| `confirm` \| `recruit`
- `decision_rationale`: string

Full field definitions: [`../../schemas/p02-output.schema.json`](../../schemas/p02-output.schema.json).

## Decision rules

Let `delegate_min_score` = D, `confirm_band_min` = C (from `matching_config`).

- `best.score >= D` and `best.confidence` is not `low` → `delegate`.
- `C <= best.score < D` → `confirm` (present top 2 and recommendation; apply probation +5 margin rule from `03` when applicable).
- `best.score < C` → `recruit`.

**Probation:** If best candidate `on_probation`, require **+5** score margin over second place to auto-`delegate`; else `confirm`.

## Quality gates

- No P02b row without **description- or excerpt-aligned** evidence.
- Subscores must **sum to `score`** (integer, 0–100).
- If all shortlist scores `< C`, decision must be `recruit`.
- **Keyword stuffing:** penalize `competency_coverage` and `outcome_fit` when only tokens match, not deliverables.

## Failure modes

- **Description-only matching** — If body excerpts missing, flag `confidence: medium` or `low` for scores near thresholds.
- **Stale registry** — Honor `registry_status`; if `install_path` missing, prefer `low` confidence on borderline.
