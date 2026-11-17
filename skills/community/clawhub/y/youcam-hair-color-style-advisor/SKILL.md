---
name: hair-color-style-advisor
description: >-
  Recommend a hairstyle and hair color based on the user's face shape and skin tone,
  then preview them with YouCam (Perfect Corp) AI. Use for "推薦髮型", "換髮色",
  "hairstyle advice", "hair color try-on". Do NOT use for hair health diagnostics
  (that's hair-diagnostics), skin, makeup, or clothes.
version: 1.1.2
requirements:
  credentials:
    - name: YOUCAM_API_KEY
      source: env | credentials.json (in the skill root, next to SKILL.md)
  network:
    - yce-api-01.makeupar.com
  apis:
    - face-attr-analysis
    - skin-tone-analysis
    - hair-transfer
    - hair-color
  permissions:
    - type: exec
      commands: [python]
---

# Hair Color & Style Advisor

An analysis + generation skill: analyze face shape and skin tone, then recommend and **preview**
a hairstyle and/or hair color.

## When to trigger
When the user wants a hairstyle/color recommendation or try-on. For hair-health diagnostics,
hand off to hair-diagnostics.

## Ask first (this skill has multiple generation options) and state cost
Before generating, ask the user what they want and tell them the credit cost of each:
- **Restyle (change hairstyle)** — `hair-transfer`
- **Recolor (change hair color)** — `hair-color`
- **Both**
Get costs with `python scripts/youcam_core.py cost --feature hair-transfer` and `--feature hair-color`
(plus the analysis features if you run them), tell the user, and only run what they choose.

## Get the latest API spec (do this every run)
- Facial attributes: https://docs.perfectcorp.com/reference/ai_face_analyzer.md
- Skin tone: https://docs.perfectcorp.com/reference/ai_skin_tone_analysis.md
- Restyle: https://docs.perfectcorp.com/reference/ai_hairstyle.md (latest may be hair-transfer v2.1)
- Recolor: https://docs.perfectcorp.com/reference/ai_hair_color.md
Pass `--version` if newer than `api-fallback.yaml`.

## Prerequisites
1. A clear, **front-facing** selfie that shows the hair.
2. Run `python scripts/youcam_core.py validate-key` (0 credits) to confirm the key. If it is not set,
   tell the user to get one at <https://yce.perfectcorp.com/api-console> and set the
   `YOUCAM_API_KEY` env var, or create `credentials.json` in the skill root (see
   `credentials.example.json` for the format).

## Flow
1. **Analyze** (as needed): face shape with
   `python scripts/youcam_core.py run --feature face-attr-analysis --src_file <photo> --param features='["faceShape","faceAspectRatio"]'`
   (`features` is required and picks which attributes to measure), and
   `run --feature skin-tone-analysis` for colors.
   - The face shape comes back as `faceshape`: one of Triangle, Diamond, Heart, InvTriangle,
     Oblong, Oval, Round, Square, or Unknown; `references/guide.md` has advice for Round, Oblong, Square, and Heart.
   - If it is `Unknown`, don't guess a shape. `face_aspect_ratio` comes back as `[1, r]` (ideal
     1 : 1.46): r above about 1.6 means a long face, below about 1.3 a short/wide one. Use it
     only for that long-vs-wide advice, and keep the rest general.
2. **Recommend**: use `references/guide.md` — face shape → hairstyle silhouette, skin tone →
   color family.
3. **Restyle** (hair-transfer): style source can be a preset template or a reference photo.
   - Template: list the styles with `python scripts/youcam_core.py templates --feature hair-transfer`
     (0 credits; each has an `id`, `title`, and `thumb` image; pass `--starting_token <next_token>`
     for the next page), let the user pick one, then
     `run --feature hair-transfer --src_file <photo> --param template_id=<id>`
   - Reference photo: `run --feature hair-transfer --src_file <photo> --ref_file <style.jpg>`
4. **Recolor** (hair-color): `run --feature hair-color --src_file <photo> --param preset="Honey Blonde"`
   (or custom pattern + palettes; ombre needs blend_strength / line_offset — see the doc).
5. The generation returns a result image URL in `data.results.url`.
6. If `run` prints `"task_status": "running"`, the task is still processing and
   `run` stopped waiting. Do not run it again, since that starts a new task and charges again.
   Check back with `python scripts/youcam_core.py status --feature <feature> --task_id <task_id>`,
   using the `task_id` from that output, until `task_status` is `success` or `error`. A task_id
   stays valid for 24 hours.

## Output rules
* **Return the result image URL exactly as given** (hyperlink is OK; do not modify it).
* Explain the recommendation (face shape → style, skin tone → color).
* **Always end with this note:** "This preview image is AI-generated and for reference only;
  real hairstyle/color results may vary. For coloring, consult a professional stylist."
