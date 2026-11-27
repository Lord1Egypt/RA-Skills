# Workflow, concept template, specs and prompts

## Topic analysis card

```
Title / topic:
Viewer and niche:
Promise (what the video delivers):
Emotion to trigger:
Curiosity gap (what they will want to find out):
Strongest visual (real, in the video):
Text angle (adds to the title, 1-4 words):
Brand constraints (fonts, colours, logo, face):
```

## Concept template (3 to 5, each different)

| Field | Content |
|---|---|
| Name | short label |
| Idea | one sentence |
| Subject and expression | who or what, which emotion |
| Text | 1 to 4 words (+ highlight word) |
| Layout | e.g. subject right third, text left, arrow to subject |
| Colours | base, accent, text colour |
| Assets | own photo / stock query / AI prompt / cutout needed |
| Why it might work | one line, honest, no invented stats |
| Risk | what could mislead or fail (e.g. needs a real before/after) |

End with a recommendation and a second choice, and propose which two to test.

## Spec format (thumb_compose.py)

All positions are fractions of the canvas (0 to 1).

```json
{
  "size": "youtube",
  "output": "out/thumb_a.jpg",
  "max_mb": 1.9,
  "background": {"image": "assets/bg.jpg", "focus": [0.5, 0.5], "darken": 0.25, "saturation": 1.2, "vignette": 0.4},
  "layers": [
    {"type": "image", "file": "assets/person_cutout.png", "anchor": "right", "height": 0.98, "x": 0.02,
     "outline": {"color": "#ffffff", "width": 7}, "shadow": true},
    {"type": "text", "text": "Stop doing this now", "box": [0.04, 0.08, 0.58, 0.62], "font": "Anton",
     "highlight": {"words": ["now"], "color": "#FFE600"}, "max_lines": 3},
    {"type": "shape", "shape": "arrow", "xy": [0.45, 0.85, 0.62, 0.55], "color": "#FF2D2D", "width": 16, "shadow": true},
    {"type": "shape", "shape": "badge", "xy": [0.04, 0.76, 0.3, 0.88], "color": "#E01010", "text": "NEW"}
  ]
}
```

- Backgrounds: `image`, or `gradient: ["#0b1020", "#ff3d00"]` with `angle`, or `color`.
- Image layers: `anchor` left/right/center, `height` or `width` as a fraction, `x`/`y` **margins from the anchor/valign edge** (0 = touching that edge; they are not positions, so `anchor: right` with `x: 0.9` pushes the image off the left side), `valign`, effects `outline`, `glow`, `shadow`. `thumb_check.py` fails a render whose image layer is mostly off the canvas.
- A photo without transparency pasted as a layer shows as a rectangle; without a cutout tool, use it as the `background` instead.
- Text auto-fits its box: it picks the largest size that fits within `max_lines`. If it errors, shorten the text or enlarge the box.
- `font`: a font file path, or a family name that `fc-match` can find; otherwise it falls back to Anton, DejaVu Bold, Liberation Bold, Impact or Arial Bold when present. Always use fonts whose licence allows the use (Anton and Montserrat are open-licence Google Fonts).
- `variants` swaps the first text layer's text (`--texts "A|B"`), applies colour themes (dark, bright, warm, cool) and mirrors the layout (`--flip`). Texts vary fastest, so `--max` keeps every text; it prints a note when combinations are cut. Themes override your layer colours.
- Paths in a spec are relative to the spec file. A `.layout.json` is written next to every render; `thumb_check.py` uses it for text checks.
- Shorts: `"size": "shorts"` (1080x1920) and design the layout for the vertical frame (text in the middle band).

## Writing image prompts (for AI generators)

Use `thumb_assets.py prompt --subject ... --emotion ... --setting ... --palette ...`, or follow this structure: subject and action, expression, setting, style (sharp, high contrast, saturated photo/illustration), lighting (rim light, strong separation), colour palette, composition (subject on one third, the other third empty for text, one focal point), 16:9, and "no text, no logos, no watermark". Generate backgrounds, objects and scenes; add all text yourself. Iterate on one change at a time. Do not prompt for a real person's likeness or a celebrity.

## Brand kit (keep in the project folder as brand.json)

```json
{"fonts": ["Anton"], "colors": {"base": "#0B1020", "accent": "#FFE600", "text": "#FFFFFF", "stroke": "#000000"},
 "logo": "assets/logo.png", "subject_side": "right", "outline": {"color": "#FFFFFF", "width": 7},
 "notes": "Keep text to 3 words; one accent word in yellow."}
```

Copy these values into every spec so a series stays consistent.

## Folder layout and deliverables

```
thumbs/
  brand.json
  assets/        photos, cutouts, backgrounds, attribution.json
  specs/         one JSON per concept
  out/           renders, .layout.json files, variants/sheet.jpg, prev/preview.png
```

Deliver: the recommended final image (plus runner-up), the variants sheet, the concept table, credits for any stock photos, and the A/B plan. If the user asks for a design they will keep editing, give the specs and the PNG; if they want to edit by hand, suggest Photopea or GIMP with the cutout PNG and background.
