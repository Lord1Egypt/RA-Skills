# Propose: 3 directions, mood images, a simple mock

Use this when the student wants to see ideas before anything is built ("propose some looks", "show me options", 3 directions).

## 1. Three directions

Follow `directions.md` for making them truly different. For each direction write: a feeling-based name, one line, fonts, corner radius, and light AND dark colours (`bg, surface, text, muted, border, accent, onAccent`). Every direction is a pair from the start: the student is choosing a look, not a mode.

## 2. Optional mood image (cheap)

Ask once: "Want a quick mood picture for each idea? It costs about one cent each." Skip if they say no or no image connector is connected.

- At most 1 image per direction (2 only if they ask). Never more than 6 in one round.
- Check the price before you generate: list the connector's tools with GetDynamicTools and preflight where it can (Higgsfield `generate_image` with `get_cost: true` submits nothing). Pick the cheapest model that can do it.
- Measured October 2026: Runway `generate_image` with `recraft-v4.1-flash` or `muse-image` = 1 credit per image (about $0.01); `seedream-5-flash` and `p-image-ideogram` = 2 credits. Higgsfield `gpt_image_2_5` preflighted at 0.25 credits per image. Prefer whichever is cheapest for the account; prices change, so preflight every time.
- Prompt for ONE mood image of the app's main screen in that direction: palette, type feel, materials, lighting. No brand names, no artist names, no readable text needed. It is mood only; the student chooses from the mock, not from the picture.
- Save images to `<appDir>/.shipyard/design/mood-<a|b|c>.png` (that folder is not committed).
- Never use video generation here; it costs many times more.

## 3. The simple mock and comparison page

Write `<appDir>/.shipyard/design/directions.json`:

```json
{ "app": "Recall", "directions": [
  { "id": "direction-a", "name": "Quiet paper", "description": "Warm, calm, made for reading.",
    "font": "Georgia, serif", "radius": "4px", "moodImage": "mood-a.png",
    "sample": { "title": "Today", "line": "3 notes to review", "action": "Review", "items": ["Lecture 4", "Reading list", "Ideas"] },
    "tokens": { "light": { "bg": "#f6f1e7", "surface": "#fffaf0", "text": "#1d1b16", "muted": "#5f584b", "border": "#d9cfbd", "accent": "#9a3412", "onAccent": "#ffffff" },
                "dark":  { "bg": "#14120e", "surface": "#1d1a15", "text": "#efe8da", "muted": "#a89f8e", "border": "#2e2a23", "accent": "#fb923c", "onAccent": "#1a0d03" } } }
]}
```

Use the app's real words in `sample`. Then:
`node "${CLAUDE_PLUGIN_ROOT}/scripts/theme-packs.mjs" mock <appDir>/.shipyard/design/directions.json --out <appDir>/.shipyard/design/directions.html`

It refuses directions with a missing mode or low contrast. Open the page (or screenshot it) and show it. For a richer view of the real app, `design-directions.mjs` (SKILL.md 3c) still works after this.

## 4. The student picks

They say `Shipyard: use direction B for <App>`. Build that one only: see SKILL.md "Build the chosen look".
