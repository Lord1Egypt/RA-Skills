# screencast-studio

Auto-record narrated demo videos of any web UI — so you can test, share, and (eventually) iterate on what you vibe-coded.

https://github.com/user-attachments/assets/5bacd549-4506-4174-b56f-77175e4646b8

> ~2-min demo. White cursor + click ripples + subtitles are ffmpeg overlays. The blurred patches in the sidebar are persistent masks (v0.2.0 feature), declared once in CONFIG and applied as the top composition layer.

## Why this exists

After you vibe-code a feature, how do you test what you actually built? How do you vibe-show it to a teammate? Manual screen recording is friction every time. This turns a declarative Playwright script (`sub` / `click` / `scroll`) into a polished demo video — narrated, cursor-tracked, mask-protected — so the cost of "make a demo" drops from minutes to one `npm run ship`.

The bigger vision: **build products by scrolling demos.** You see a version, tell the AI what's off, swipe to the next take, stop when one matches what you wanted — scrolling demos *is* the dev loop, not just a way to review one. Vibe coding × vibe testing × vibe iteration.

## How it works

The cursor isn't real. Playwright headless has no mouse, so `record.js` just drives the page and logs every click and subtitle as it goes. `postprocess.js` reads that log and ffmpeg-overlays a cursor that glides to each target, drops a Material ripple on click, and burns in subtitles. Sensitive UI regions can be declared in CONFIG and they're blurred automatically as the top composition layer.

Output:

- `final.mp4` — h264, cursor overlay + click ripples + burned-in subtitles + persistent-mask blur
- `review/{flow,visual,coverage,sensitive}/*.png` — 4-pass screenshot set for visual + privacy QA

## Quick start

Tell Claude:

> 用 screencast-studio 给我录个 demo

It scaffolds `record.js`, `postprocess.js`, `review.js`, and the rest. Then:

```bash
npm install
npx playwright install chromium
npm run setup
npm run login   # only if your target needs auth
# declare PERSISTENT_MASKS + edit the flow in record.js
npm run ship
```

`ship` runs record → render → deploy → review → clean. ~3–5 min for a 2-min demo. The review phase has no progress indicator, so don't assume it hung.

## Authoring

Stage flow lives inside `record.js`:

```js
await sub('Open the project list');
const navProj = page.locator('a[href="/projects"]').first();
await click(navProj, 'Click "Projects" in sidebar');
await sub('Multiple projects in flight');
await scroll(400, 2);
await sub('Scroll to see more');
```

Five helpers — `sub` / `click` / `scroll` / `hold` / `tryStep` — cover ~95% of cases. Full pattern guide: [`examples/walkthrough-flow.md`](examples/walkthrough-flow.md).

## Persistent masks (privacy)

Declare sensitive UI regions in `record.js` CONFIG; they get blurred for the entire video as the top composition layer:

```js
const PERSISTENT_MASKS = [
  { selector: '.user-badge',  label: 'username' },
  { selector: 'header .logo', label: 'logo' },
  { box: { x: 0, y: 820, w: 220, h: 80 }, label: 'sidebar-bottom' },
];
```

`selector` masks resolve once after first navigation (best for `position: fixed`/`sticky` elements); `box` masks are fixed coordinates (use these for retroactive coverage — edit + `npm run render` without re-recording). Default blur is `boxblur=lr=20:lp=2:cr=15:cp=2` (chroma capped per ffmpeg); tune in `postprocess.js` if text is still legible. After every ship, **read `review/sensitive/`** — it crops each mask region for blur verification and samples full frames every 10s for unmasked-PII detection.

## Prerequisites

Node 18+. Playwright and ffmpeg-static install via npm; `npx playwright install chromium` once. CJK fonts ship with Windows and macOS; on Linux, `apt install fonts-noto-cjk` (or your distro's equivalent). Full list: [`references/prerequisites.md`](references/prerequisites.md).

## Gotchas

Subtitle count ≠ correctness, and ship success ≠ privacy. Subtitles fire on a timer; they keep going even if a click missed and the page never advanced. Masks are also blind to UI states they didn't cover. Always read all 4 review passes after `ship` — `flow` / `visual` / `coverage` / `sensitive`. More in [`references/known-pitfalls.md`](references/known-pitfalls.md).
