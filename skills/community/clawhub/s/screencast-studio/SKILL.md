---
name: screencast-studio
description: Auto-record narrated demo videos of any web UI from a Playwright-driven walkthrough — primary use case is the vibe-coding test loop (you just shipped a feature with AI help and need to verify it / vibe-show it / iterate on it without manual screen recording). Output is a final.mp4 (synthetic cursor lerp + Material click ripples + burned-in subtitles + optional persistent mask regions for sensitive UI) plus a 4-pass review screenshot set for visual + privacy QA. Activate when the user wants to test or share something they just vibe-coded, or asks for a polished walkthrough / OSS feature demo / bug repro screencast / tutorial recording.
version: 0.2.1
---

# Screencast Studio

Auto-record narrated demo videos of any web UI — so the user can **test, share, and iterate** on what they just vibe-coded.

The primary use case: the user has just shipped a feature (often with AI help), and wants to verify it visually + show it to a teammate without manually screen-recording every time. The longer-term vision is **building products by scrolling demos** — see a version, tell the AI what's off, swipe to the next take, stop when one matches what you wanted. Scrolling demos *is* the dev loop, not just a way to review the output.

The technical trick: **a Playwright headless recording has no real cursor**. The visual cursor + click ripples + subtitles you see in the final video are **ffmpeg overlays composed from a structured events log**, not real mouse events. This decoupling lets the recording script stay declarative ("click this, narrate that") while the production-quality visuals (smooth cursor lerp, ripple flash, subtitle timing) come for free from the post-processor.

## When to use

Activate when the user asks for any of:

- **Vibe coding test loop** — they just shipped a feature with AI help and want to verify it visually or share it with a teammate (this is the *primary* trigger)
- A polished **product walkthrough video** of a web app
- An **OSS feature demo** for a README or release announcement
- A **bug repro screencast** with narrated steps
- A **tutorial / onboarding video** showing how to do something in a browser-based UI
- Anything where the user said "vibe show / vibe demo / 测一下我刚做的 / 给同事看看 / 录 demo / 录视频 / screencast / walkthrough video / 演示视频"

Don't activate when:

- The user wants to record **non-browser content** (use OBS / native screen recorders)
- A single screenshot or a static image would suffice
- The user wants to record **real mouse motion** (this skill draws a synthetic cursor)
- The target UI is mobile-only (Playwright supports mobile emulation, but the cursor + ripple visuals are tuned for desktop viewports)

## Pipeline overview

```
gen-cursor + gen-ripple  →  cursor.png, ripple.png                    (one-time)
login                    →  storageState.json + page summary
record                   →  raw.webm + events.json (incl. mask events)
postprocess              →  final.mp4 + subs.srt   (mask blur applied)
deploy                   →  output/screencast-{stamp}.mp4
review                   →  review/{flow,visual,coverage,sensitive}/*.png
clean                    →  drop scratch files
```

`npm run ship` runs record → postprocess → deploy → review → clean as one command.

## Bootstrapping a new project

When the user says they want to record a demo for some web app, do this:

### 1. Gather what you need to know

Ask the user (briefly, ideally in one round):

- **Target URL** (the BASE — local `http://localhost:3000` or remote)
- **Login path** if not `/login`
- **Working directory** for the demo project (e.g. `D:\AI\my-demo` or `~/projects/my-demo`)
- Whether they need a **deploy directory** (default is `./output/`)
- Viewport size if other than `1440x900`

### 2. Scaffold the project

Copy templates into the working directory:

```
templates/record.js          → <working-dir>/record.js
templates/postprocess.js     → <working-dir>/postprocess.js
templates/review.js          → <working-dir>/review.js
templates/login.js           → <working-dir>/login.js
templates/gen-cursor.js      → <working-dir>/gen-cursor.js
templates/gen-ripple.js      → <working-dir>/gen-ripple.js
templates/deploy.js          → <working-dir>/deploy.js
templates/clean.js           → <working-dir>/clean.js
templates/package.json       → <working-dir>/package.json
```

Then in the working directory:

```bash
npm install
npx playwright install chromium
```

### 3. Configure

The templates already accept these env vars (no code edit needed for most cases):

- `SCREENCAST_BASE` — target URL
- `SCREENCAST_LOGIN_PATH` — defaults to `/login`
- `SCREENCAST_VIEWPORT_W` / `SCREENCAST_VIEWPORT_H` — defaults 1440/900
- `DEPLOY_DIR` — defaults to `./output/`
- `DEPLOY_PREFIX` — defaults to `screencast`
- `SUBTITLE_FONT` — overrides the platform-detected CJK font

For a one-off, edit `record.js` lines 22-26 directly.

### 4. Run setup + (optionally) login

```bash
npm run setup      # generates cursor.png and ripple.png
npm run login      # opens a real browser; user logs in manually
```

**Skip `npm run login` if your target page is public** (no auth needed). `record.js` will run without a `storageState.json` if the file doesn't exist — the demo just won't have any logged-in session. The `npm run login` step exists specifically for apps behind a login screen.

After `npm run login` (when used), `post-login-summary.json` will contain visible nav / heading / button text. **Read this file before authoring the stage flow** — it tells you what selectors are available without poking the live UI.

### 5. Configure persistent masks (REQUIRED — privacy gate)

**Before authoring the stage flow, you MUST ask the user about sensitive UI regions to mask.** This is a hard requirement, not an optional polish step. If the demo will be shared (OSS / X / public README), unmasked PII in the recording is hard to retract — git history rewrites + CDN takedown tickets are painful.

Read `post-login-summary.json` and `post-login.png` for context, then ask the user something like:

> Before I start the recording, I want to mask sensitive UI regions. Looking at this app, here's what I notice that often needs masking — please confirm or correct:
>
> - Top-left logo / brand (if internal product)
> - Sidebar user badge / username / avatar (bottom-left in many SPAs)
> - Footer version number (e.g. `v1.x.x-beta`)
> - Real names, emails, internal project codenames
>
> Which of these should be blurred? Anything else specific to your demo (real customer data, internal task IDs, business strategy text)?

Then edit `PERSISTENT_MASKS` in `record.js` (top CONFIG block):

```js
const PERSISTENT_MASKS = [
  { selector: '.user-badge',  label: 'username' },         // resolved once at startup
  { selector: 'header .logo', label: 'logo' },
  { box: { x: 0, y: 820, w: 220, h: 80 }, label: 'sidebar-bottom' },  // fixed coordinates
];
```

**Selector vs box**:
- **Selector** is auto-resolved against the live DOM after first navigation. Element MUST be `position: fixed` or `sticky` — otherwise the captured boundingBox drifts when the page scrolls. If the resolver detects non-fixed positioning, it warns in the log; switch to `box` in that case.
- **Box** is fixed `{x, y, w, h}` in viewport coordinates. Use this when selectors are unreliable, or to cover a known-stable region (e.g. footer area regardless of element).

If the user says "no masks needed" (e.g. demo is on a generic public site with no PII), leave the array empty — the recording proceeds without any blur. Don't lecture.

### 6. Author the stage flow

Edit the body of the `try { ... }` block in `record.js` (search for `STAGE FLOW`). The page is already on `BASE` when your flow starts (record.js handles first navigation + mask resolution before the STAGE FLOW block) — your code does NOT need to call `page.goto(BASE)` again.

Use the helpers documented in [references/helpers-api.md](references/helpers-api.md). For a fuller pattern guide see [examples/walkthrough-flow.md](examples/walkthrough-flow.md).

### 7. Ship

```bash
npm run ship
```

This runs the full pipeline (record → postprocess → deploy → review → clean). On a 2-minute demo with ~20 clicks, expect:

- record: ~2-3 minutes (real-time playthrough plus dwell times)
- postprocess: ~30-60 seconds (ffmpeg compositing — slightly longer per persistent mask)
- review: ~30-60 seconds (n × ffmpeg seek+frame extraction; **no progress indicator, just waits silently — that's normal**)

### 8. Privacy + visual review (REQUIRED — do not skip)

After `npm run ship` completes you MUST read the review screenshots before declaring the demo done. Subtitle counts and ship success do NOT prove the recording is shippable.

**Read all 4 review passes**:

1. `review/flow/click-XX-*.png` — sample clicks with high `y` or large delta from previous click; confirm cursor is on target
2. `review/visual/sub-XX.png` — every subtitle: does the text match what UI shows?
3. `review/coverage/stage-XX.png` — for any `tryStep` stage: did it actually execute?
4. **`review/sensitive/` — read EVERY image** and answer:
   - For each `mask-XX-*.png` (cropped to mask region): is the area unreadable / blurred to noise?
   - For each `scan-XX-*.png` (full frame at 10s intervals): is there ANY PII visible? Look for usernames, real names, emails, UUIDs, version numbers, internal project codenames, business strategy text, real customer data.

**If the sensitive pass surfaces unmasked PII**: STOP. Add a `box` mask to `PERSISTENT_MASKS` (you don't need a selector for retroactive masks — just measure coordinates from the offending scan-XX.png). Then run **only** `npm run render && npm run review:sensitive` (no need to re-record — the original `events.json` is reused). Iterate until `review/sensitive/` is clean.

**If the user explicitly said "no masks needed" upfront** but you still find PII in `scan-XX.png`: do NOT silently ship. Flag it back to the user and ask how to proceed.

See [references/known-pitfalls.md](references/known-pitfalls.md) for other things to watch for.

## Authoring helpers (quick reference)

Inside the `try { ... }` block of `record.js`:

| Helper | What it does |
|---|---|
| `await sub('subtitle text')` | Adds a subtitle event + holds the page for a CJK-aware duration |
| `await click(locator, '操作描述')` | Cursor moves to target, dwells, clicks, dwells (full ceremony) |
| `await scroll(deltaY, ticks=1)` | Wheel-scrolls main content area (mouse parks in viewport center first) |
| `await hold(ms=400)` | Explicit pause |
| `await tryStep('name', async () => { ... })` | Non-fatal stage; if it throws, log and continue |
| `page` | The underlying Playwright Page (escape hatch for anything the helpers don't cover) |

Full API in [references/helpers-api.md](references/helpers-api.md).

## Authoring tips

- **Stage flow is a sequence of `sub` + `click` + `scroll` + `hold` calls.** Think of `sub` as the narrator's voice and `click`/`scroll` as the action.
- **Wrap risky steps in `tryStep`** if the UI surface depends on data that may not exist (e.g. an empty list view has no rows to click).
- **Don't fight Playwright's auto-waiting** — selectors should target visible elements; if you need to wait for something to appear, use `await locator.waitFor({ state: 'visible' })` before clicking.
- **Prefer text-based selectors with `exact: true`** for robustness:
  - `page.getByText('Save', { exact: true })` ✓
  - `page.locator('text=Save')` ✗ (matches "Save", "Saved", "Save changes" — substring match)
- **Subtitles narrate, not describe**. "进入项目模块" is better than "I am clicking the projects tab".

## Prerequisites

See [references/prerequisites.md](references/prerequisites.md) for the full list. Summary:

**Auto-installed by `npm install`**: playwright, ffmpeg-static, fluent-ffmpeg

**OS-level**: Node 18+; chromium binary (one-time `npx playwright install chromium`); a CJK font (Microsoft YaHei on Windows / PingFang SC on macOS / Noto Sans CJK SC on Linux — the postprocess auto-detects)

**Project-specific**: the target web app's URL and login credentials; optionally test files for upload stages and a deploy directory

## Known pitfalls

See [references/known-pitfalls.md](references/known-pitfalls.md). The big ones:

- **Cursor disappears off-frame** if a click target is below the viewport — the `click` helper auto-scrolls into view, but if you bypass it (e.g. raw `locator.click()`), the synthetic cursor will fly to coordinates outside the recorded frame.
- **Wheel scrolls the wrong container** if you don't park the mouse first — the `scroll` helper does this, but raw `page.mouse.wheel(0, dy)` from cold-start will scroll whatever element is at (0, 0) (usually the sidebar).
- **`text=...` is substring match** — use `getByText(s, { exact: true })` for precision.
- **Subtitle count ≠ done.** `report.txt` shows the events fired, not that the demo *looks correct* and not that PII is hidden. The 4-pass review screenshots (flow / visual / coverage / sensitive) exist precisely so you (or the user) can verify visually after every ship.
- **Mask drift on scrolling elements** — `selector`-based masks capture boundingBox once. If the element is not `position: fixed` / `sticky`, the mask stays put while the element moves. Use a `box` covering the worst-case viewport position instead.

## Reference docs

- [prerequisites.md](references/prerequisites.md) — full setup checklist incl. cross-platform
- [helpers-api.md](references/helpers-api.md) — full helper API + tuning knobs
- [events-schema.md](references/events-schema.md) — events.json structure + how postprocess consumes it
- [ffmpeg-pipeline.md](references/ffmpeg-pipeline.md) — what the post-processor actually does
- [known-pitfalls.md](references/known-pitfalls.md) — every pitfall encountered + how to avoid

## Example

- [examples/walkthrough-flow.md](examples/walkthrough-flow.md) — walkthrough of a real demo, showing every stage pattern.
