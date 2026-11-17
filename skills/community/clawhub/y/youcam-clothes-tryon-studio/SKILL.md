---
name: clothes-tryon-studio
description: >-
  Virtual clothes try-on studio using YouCam (Perfect Corp) AI. Swap outfits onto the
  user's photo, optionally change the background, and optionally turn the result into a
  short motion video (turn / runway / pose). Use for "換衣", "虛擬試穿", "outfit try-on",
  "try on clothes". Do NOT use for makeup, hair, or skin analysis.
version: 1.1.2
requirements:
  credentials:
    - name: YOUCAM_API_KEY
      source: env | credentials.json (in the skill root, next to SKILL.md)
  network:
    - yce-api-01.makeupar.com
  apis:
    - cloth-v4
    - bg-replace
    - image-to-video
  permissions:
    - type: exec
      commands: [python]
---

# Clothes Try-on Studio

A generation skill: try on clothes, optionally change the background, optionally turn the result
into a short motion video.

## When to trigger
When the user wants to try clothes on virtually. For makeup, hair, or skin, hand off to the
matching skill.

## Ask first (this skill has multiple generation steps) and state cost
Before generating, ask the user which steps they want and tell them the credit cost of each:
- **Try on clothes** (`cloth-v4`) — required base step
- **Change background** (`bg-replace`) — optional
- **Motion video** (`image-to-video`) — optional; note video is billed per second
Get costs with `python scripts/youcam_core.py cost --feature cloth-v4` (and `--feature bg-replace`,
`--feature image-to-video`), tell the user the total, and only run what they choose.

## Get the latest API spec (do this every run)
- Clothes: https://docs.perfectcorp.com/reference/ai_clothes.md (latest engine cloth-v4)
- Background change: https://docs.perfectcorp.com/reference/ai_photo_background_change.md
- Video generator: https://docs.perfectcorp.com/reference/ai_video_generator.md
Pass `--version` if newer than `api-fallback.yaml`.

## Prerequisites
1. A photo of the person (full-body or upper-body) plus one garment reference image (product or
   worn photo) or a template_id.
2. Run `python scripts/youcam_core.py validate-key` (0 credits) to confirm the key. If it is not set,
   tell the user to get one at <https://yce.perfectcorp.com/api-console> and set the
   `YOUCAM_API_KEY` env var, or create `credentials.json` in the skill root (see
   `credentials.example.json` for the format).

## Flow (only the chosen steps)
1. **Try on** (cloth-v4):
   ```
   python scripts/youcam_core.py run --feature cloth-v4 --src_file <person.jpg> --ref_file <garment.jpg> \
       --param garment_category=full_body
   ```
   (or use a template: `--param template_id=<id>`; confirm the exact `garment_category` value from
   the latest doc — see Notes.)
2. **(Optional) Change background** (bg-replace): on the result or original image,
   `run --feature bg-replace --src_file <img> --param type=prompt --param prompt="A sunny beach"`
   or use a preset background: list them with `python scripts/youcam_core.py templates --feature bg-replace`
   (0 credits; each has an `id`, `title`, and `thumb` image; pass `--starting_token <next_token>`
   for the next page), let the user pick one, then
   `run --feature bg-replace --src_file <img> --param type=template --param template_id=<id>`.
3. **(Optional) Motion video** (image-to-video):
   `run --feature image-to-video --src_file <img> --param resolution="720" --param dst_duration=5 --param prompt="turn around / runway walk"`
4. Each generation returns a result image/video URL in `data.results.url`.
5. If `run` prints `"task_status": "running"`, the task is still processing and
   `run` stopped waiting. Do not run it again, since that starts a new task and charges again.
   Check back with `python scripts/youcam_core.py status --feature <feature> --task_id <task_id>`,
   using the `task_id` from that output, until `task_status` is `success` or `error`. A task_id
   stays valid for 24 hours.

## Output rules
* **Return the result image/video URL exactly as given** (hyperlink is OK; do not modify or
  shorten it).
* Video can take longer than `run`'s default wait. If it returns `running`, check back with
  `status` as in step 5.
* **Always end with this note:** "This try-on image/video is AI-generated and for reference only;
  actual fit and appearance may vary."

## Notes
`cloth-v4` `garment_category` is confirmed for `full_body`; the upper/lower-body token spelling is
not yet 100% confirmed, so verify it against the latest doc parameter table before running (see
the handoff GAPS).
