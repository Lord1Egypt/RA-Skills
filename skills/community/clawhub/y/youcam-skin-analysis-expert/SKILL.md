---
name: skin-analysis-expert
description: >-
  Analyze a person's skin from a single selfie using YouCam (Perfect Corp) AI.
  Returns 16 skin-condition scores plus skin type, as a readable report. Use when
  the user wants a skin analysis / skin report / skin score — incl. "幫我看膚質",
  "膚況分析", "how's my skin", "skin report". Do NOT use for skin-tone/facial
  attributes (that's facial-consultant), makeup, or hair.
version: 1.1.2
requirements:
  credentials:
    - name: YOUCAM_API_KEY
      source: env | credentials.json (in the skill root, next to SKILL.md)
  network:
    - yce-api-01.makeupar.com
  apis:
    - skin-analysis
  permissions:
    - type: exec
      commands: [python]
---

# Skin Analysis Expert

An analysis skill that calls one API (`skin-analysis`). You (the agent) run the flow described
here through `scripts/youcam_core.py`.

## When to trigger
When the user wants to understand their skin condition / get a skin report or score.
If they want skin tone, facial attributes, makeup, or hair, hand off to the matching skill.

## Get the latest API spec (do this every run)
Read this documentation section and open its **latest version** subpage to get the current
endpoint / parameters / response fields:
https://docs.perfectcorp.com/reference/ai_skin_analysis.md
(e.g. the latest may be `.../ai_skin_analysis/v2.1`. If it is newer than `api-fallback.yaml`,
pass `--version` when calling.)

## Prerequisites
1. A clear, front-facing, single-person selfie with even lighting (jpg/jpeg/png).
2. Run `python scripts/youcam_core.py validate-key` (0 credits) to confirm the key. If it is not set,
   tell the user to get one at <https://yce.perfectcorp.com/api-console> and set the
   `YOUCAM_API_KEY` env var, or create `credentials.json` in the skill root (see
   `credentials.example.json` for the format).
3. Before running, check the cost and tell the user how many credits it will use:
   `python scripts/youcam_core.py cost --feature skin-analysis`
   (skin-analysis is tiered by SD/HD and number of concerns.)

## Pre-run questionnaire (ask all 3 before running)

Ask the user these 3 questions **before** calling the API. Collect all answers first, then run once.

**Q1 — Analysis tier**
> Would you like **HD** (high-detail, regional breakdowns) or **SD** (standard) analysis?

**Q2 — Concerns to analyse**
> Which skin concerns would you like to check?
> Choose any combination, or say **"all"** for the full set.
>
> | # | Concern | HD action | SD action |
> |---|---------|-----------|-----------|
> | 1 | Spots (age spots) | `hd_age_spot` | `age_spot` |
> | 2 | Wrinkles | `hd_wrinkle` | `wrinkle` |
> | 3 | Texture | `hd_texture` | `texture` |
> | 4 | Dark circles | `hd_dark_circle` | `dark_circle_v2` |
> | 5 | Redness | `hd_redness` | `redness` |
> | 6 | Pores | `hd_pore` | `pore` |
> | 7 | Acne | `hd_acne` | `acne` |
> | 8 | Oiliness | `hd_oiliness` | `oiliness` |
> | 9 | Hydration | `hd_moisture` | `moisture` |
> | 10 | Firmness | `hd_firmness` | `firmness` |
> | 11 | Droopy upper eyelid | `hd_droopy_upper_eyelid` | `droopy_upper_eyelid` |
> | 12 | Droopy lower eyelid | `hd_droopy_lower_eyelid` | `droopy_lower_eyelid` |
> | 13 | Eye bags | `hd_eye_bag` | `eye_bag` |
> | 14 | Radiance | `hd_radiance` | `radiance` |
> | 15 | Tear trough | `hd_tear_trough` | `tear_trough` |
> | 16 | Skin type | `hd_skin_type` | `skin_type` |
>
> Note: HD and SD actions **cannot be mixed** in a single call.

**Q3 — Image output style**
> How would you like the result images?
> - **Overlay** — the detection mask blended onto your photo (returns .jpg)
> - **Mask** — the raw detection mask only (returns .png, default)

## Run

Always use `format=json`. Build the command from the user's answers to Q1–Q3:

```
python scripts/youcam_core.py run --feature skin-analysis --src_file <photo> \
    --param format=json \
    --param dst_actions='[<actions chosen in Q2, matching tier from Q1>]' \
    --param miniserver_args='{"enable_mask_overlay": <true if overlay, false if mask>}'
```

Example (HD, all concerns, overlay):
```
python scripts/youcam_core.py run --feature skin-analysis --src_file photo.jpg \
    --param format=json \
    --param dst_actions='["hd_wrinkle","hd_pore","hd_texture","hd_acne","hd_redness","hd_oiliness","hd_moisture","hd_radiance","hd_firmness","hd_dark_circle","hd_eye_bag","hd_tear_trough","hd_droopy_upper_eyelid","hd_droopy_lower_eyelid","hd_age_spot","hd_skin_type"]' \
    --param miniserver_args='{"enable_mask_overlay": true}'
```

If `run` prints `"task_status": "running"`, the task is still processing and
`run` stopped waiting. Do not run it again, since that starts a new task and charges again.
Check back with `python scripts/youcam_core.py status --feature <feature> --task_id <task_id>`,
using the `task_id` from that output, until `task_status` is `success` or `error`. A task_id
stays valid for 24 hours.

It returns scores. Interpret them with `references/interpretation.md` (note the direction
of `ui_score` vs `raw_score`) and assemble the report with `references/output-format.md`.

## Output rules
* Follow the structure in `references/output-format.md` exactly:
  1. **3 lowest-scoring concerns** (worst first) — with scores, star ratings, actionable advice, and their images.
  2. **3 highest-scoring concerns** (best first) — with scores, star ratings, positive note, and their images.
  3. **Overall results** — text only: skin type, full concern score table, and overall impression paragraph. No images.
  4. **Closing disclaimer** (required, verbatim from output-format.md).
* Report scores as returned (`ui_score` only); never invent conditions not present in the response.
* If the API returns an error code (e.g. photo not compliant), give retake guidance instead of
  forcing a result.
