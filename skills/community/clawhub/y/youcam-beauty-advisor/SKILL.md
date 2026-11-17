---
name: beauty-advisor
description: >-
  Recommend and preview makeup looks based on the user's face shape and skin tone,
  using YouCam (Perfect Corp) AI. Analyzes the selfie, suggests suitable looks, then
  renders a virtual makeup try-on image. Use for "推薦妝容", "幫我上妝", "makeup look",
  "virtual makeup". Do NOT use for skin-condition scoring, hair, or clothes.
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
    - makeup-vto
    - look-vto
  permissions:
    - type: exec
      commands: [python]
---

# Beauty Advisor

An analysis + generation skill: analyze face shape and skin tone, then recommend and **preview**
a makeup look. Run the flow here through `scripts/youcam_core.py`.

## When to trigger
When the user wants a makeup recommendation or a virtual try-on. For skin scores, hair, or
clothes, hand off to the matching skill.

## Ask first (this skill has multiple generation options) and state cost
Before generating, ask the user which they want, and tell them the credit cost of each option:
- **Full look (preset template)** — apply a curated full-face look (`look-vto`)
- **Custom effects** — specify individual items (lip color, eyeshadow, blush, …) (`makeup-vto`)
Get costs with `python scripts/youcam_core.py cost --feature look-vto` and `--feature makeup-vto`
(and `--feature face-attr-analysis` / `--feature skin-tone-analysis` for the analysis step),
tell the user, and only run what they choose.

## Get the latest API spec (do this every run)
Read the doc section(s) for the steps you will run and open the **latest version** for endpoints
/ parameters:
- Facial attributes: https://docs.perfectcorp.com/reference/ai_face_analyzer.md
- Skin tone: https://docs.perfectcorp.com/reference/ai_skin_tone_analysis.md
- Makeup try-on (custom): https://docs.perfectcorp.com/reference/makeup_vto.md
- Full look (template): https://docs.perfectcorp.com/reference/ai_look_vto.md

## Prerequisites
1. A clear, front-facing selfie.
2. Run `python scripts/youcam_core.py validate-key` (0 credits) to confirm the key. If it is not set,
   tell the user to get one at <https://yce.perfectcorp.com/api-console> and set the
   `YOUCAM_API_KEY` env var, or create `credentials.json` in the skill root (see
   `credentials.example.json` for the format).

## Flow
1. **Analyze** (as needed): face shape and eye/lip shape with
   `python scripts/youcam_core.py run --feature face-attr-analysis --src_file <photo> --param features='["faceShape","faceAspectRatio","eyeShape","lipShape"]'`
   (`features` is required and picks which attributes to measure), and
   `run --feature skin-tone-analysis` for colors.
   - The face shape comes back as `faceshape`: one of Triangle, Diamond, Heart, InvTriangle,
     Oblong, Oval, Round, Square, or Unknown; `references/guide.md` has advice for Round, Oblong, Square, and Heart.
   - If it is `Unknown`, don't guess a shape. `face_aspect_ratio` comes back as `[1, r]` (ideal
     1 : 1.46): r above about 1.6 means a long face, below about 1.3 a short/wide one. Use it
     only for that long-vs-wide advice, and keep the rest general.
2. **Recommend**: use `references/guide.md` to pick a look/colors from face shape + skin tone.
3. **Preview** (the option the user chose):
   - Full look: list the looks with `python scripts/youcam_core.py templates --feature look-vto`
     (0 credits; each has an `id`, `title`, and `thumb` image; pass `--starting_token <next_token>`
     for the next page), let the user pick one, then
     `run --feature look-vto --src_file <photo> --param template_id=<id>`
   - Custom: `run --feature makeup-vto --src_file <photo> --param effects='[{...}]'`
     (each `effects` item is one category; see the doc's category schema and pattern catalogs)
4. The generation returns a result image URL in `data.results.url`.
5. If `run` prints `"task_status": "running"`, the task is still processing and
   `run` stopped waiting. Do not run it again, since that starts a new task and charges again.
   Check back with `python scripts/youcam_core.py status --feature <feature> --task_id <task_id>`,
   using the `task_id` from that output, until `task_status` is `success` or `error`. A task_id
   stays valid for 24 hours.

## Output rules
* **Return the result image URL exactly as given** (you may make it a hyperlink, but do not
  modify or shorten it).
* Explain the recommendation (why this look suits their face shape / skin tone).
* **Always end with this note:** "This preview image is AI-generated and for reference only;
  actual makeup results may vary by product, skin, and lighting."
