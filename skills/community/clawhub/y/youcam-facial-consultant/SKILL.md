---
name: facial-consultant
description: >-
  Analyze skin tone and facial attributes from a single selfie using YouCam
  (Perfect Corp) AI. Returns skin/eye/eyebrow/lip/hair colors plus facial feature
  shapes and golden-ratio proportions, as a readable report. Use for "測膚色",
  "臉型分析", "facial attributes". Do NOT use for skin-condition scoring (that's
  skin-analysis-expert), makeup, or hair try-on.
version: 1.1.2
requirements:
  credentials:
    - name: YOUCAM_API_KEY
      source: env | credentials.json (in the skill root, next to SKILL.md)
  network:
    - yce-api-01.makeupar.com
  apis:
    - skin-tone-analysis
    - face-attr-analysis
  permissions:
    - type: exec
      commands: [python]
---

# Facial Consultant

An analysis skill that can call two APIs. You (the agent) run the flow here through
`scripts/youcam_core.py`, and you also do the golden-ratio interpretation from the references.

## When to trigger
When the user wants their skin tone, facial features / face shape, or facial proportions.
For skin-condition scores, hand off to skin-analysis-expert.

## Ask first (this skill has multiple analyses)
Before running anything, ask the user what they want and state the credit cost of each:
- **Skin tone** — colors of skin/eyes/brows/lips/hair (`skin-tone-analysis`)
- **Facial attributes & ratios** — feature shapes, face shape, golden-ratio proportions (`face-attr-analysis`)
- **Both**
Get the per-call cost with `python scripts/youcam_core.py cost --feature skin-tone-analysis` and
`--feature face-attr-analysis`, tell the user, and only run the ones they choose.

## Get the latest API spec (do this every run)
Read the doc section(s) for the chosen analyses and open the **latest version** for the current
endpoint / parameters:
- Skin tone: https://docs.perfectcorp.com/reference/ai_skin_tone_analysis.md
- Facial attributes / ratio: https://docs.perfectcorp.com/reference/ai_face_analyzer.md
If newer than `api-fallback.yaml`, pass `--version`.

## Prerequisites
1. A clear, **front-facing**, single-person selfie.
2. Run `python scripts/youcam_core.py validate-key` (0 credits) to confirm the key. If it is not set,
   tell the user to get one at <https://yce.perfectcorp.com/api-console> and set the
   `YOUCAM_API_KEY` env var, or create `credentials.json` in the skill root (see
   `credentials.example.json` for the format).

## Run (only the chosen analyses)
```
python scripts/youcam_core.py run --feature skin-tone-analysis --src_file <photo> --param face_angle_strictness_level=high
python scripts/youcam_core.py run --feature face-attr-analysis  --src_file <photo> \
    --param face_angle_strictness_level=high \
    --param features='["eyeShape","eyeSize","eyeDistance","eyebrowShape","cheekbones","faceShape","lipShape","noseWidth","noseLength","eyeColor","lipColor","eyebrowColor","hairColor","horizontalThird","verticalFifth","faceAspectRatio","upperLipToLowerLip"]'
```
If `run` prints `"task_status": "running"`, the task is still processing and
`run` stopped waiting. Do not run it again, since that starts a new task and charges again.
Check back with `python scripts/youcam_core.py status --feature <feature> --task_id <task_id>`,
using the `task_id` from that output, until `task_status` is `success` or `error`. A task_id
stays valid for 24 hours.

Interpret colors and features with `references/guide.md`, and do the golden-ratio bucketing
yourself (buckets and golden targets are in that file).

## Output rules
* For colors, report colors only; do not infer an undertone that was not returned.
* Ratios drift slightly between runs and `faceShape` may not be returned; label ratios as
  approximate and skip missing values instead of filling them in.
* **Always end with this note:** "This is an AI-based facial analysis for reference only. It is
  not a medical or cosmetic-surgery assessment; results can vary with lighting and pose."
