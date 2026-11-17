# Real-app footage

Use this mode when the video must look exactly like the app: marketing where a rebuilt screen would feel slightly off, or a screen too rich to rebuild. Rebuilt UI (`references/scenes.md`) stays the default: it is quicker and sharper at any zoom. Footage costs more: practice pages in the app (a pull request), the recording, then composing. Tell the student that before choosing it.

Read the engine's own guide to real-app footage in `<appDir>/video/README.md` first, and `video/capture/record.mjs` and `video/src/footage.tsx`. Every path below is inside the app.

What keeps it fast: **the app is never signed in and never waits on a server.** Recording a signed-in live app costs days: sign-in automation, waits on real servers and AI, and a different timing on every take. Instead, the app gets practice pages that show its real components on made-up data, and the recording drives those.

## 1. Practice pages in the app (they only exist while building)

In a Shipyard app, put each one at `src/app/design-preview/video/<page>/page.tsx` (address `/design-preview/video/<page>`). Under `/design-preview` the app's proxy already lets the page open without sign-in while building and answers "not found" in production, and the cookie notice stays away. Copy the start of `src/app/design-preview/[id]/page.tsx`: `if (process.env.NODE_ENV === "production") notFound();`, no index for search engines, and `<AppShell signedIn isAdmin={false}>` for the signed-in look without a database.

Each page has:

- **The real components.** Import the app's own components; do not copy them. The point is the real look.
- **A fixture**: one file with the ONE made-up scenario from the script (people, items, numbers). Same values in every scene.
- **A fetch stub**: a small client component that, before the page's own code runs, replaces `window.fetch` for `/api/...` with answers from the fixture. Answer every call the page makes; make any other call fail loudly in the console so you notice it.
- **A timeline of scripted events**: a new item arriving at 2 seconds, a status changing at 5. The page plays it by itself (or on `?play=1`), so every take is the same.
- **`data-video="..."` marks** on everything the recording must find or click. Never find things by their visible text: copy and language change.

No sign-in, no database, no AI calls, no real emails, no real names. The pages are app code: they go through the app's normal branch, pull request and checks. Ask "OK to save this to GitHub?" first. Once live, open one practice address on the live site: it must say "not found".

An app Shipyard did not make (after the upgrade guide): the same idea in its stack. A route that only exists in development, renders the real components on the fixture and needs no sign-in.

## 2. Pick the window size

Check the app's layout breakpoints first (`@media` widths in its CSS, `md:` or `lg:` classes) and pick a size that shows the layout you want. An app that switches to its phone layout at 960 pixels needs a laptop take wider than that. Typical: laptop 1280 by 800, phone 390 by 844 (`phone: true`). Record at `dpr: 2` or `3` so text stays sharp when the camera zooms in. Very large recordings are scaled down by the recorder (section 6).

## 3. The capture file

`video/capture/<name>.mjs` records one take per layout and per theme. Step ids are the script's line ids.

```js
import {record} from './record.mjs';

const BASE = process.env.APP_URL; // video-capture.mjs gives it the app's address

const steps = [
  {id: 'hook', run: async (h) => { await h.pause(1200); }},
  {id: 'add', run: async (h) => {
    await h.focus('[data-video="new-recipe"]', {zoom: 1.6});
    await h.type('[data-video="new-recipe"] input', 'Lemon tart');
    await h.press('Enter');
    await h.waiting(() => h.page.waitForSelector('[data-video="recipe-card"]'));
  }},
  {id: 'share', run: async (h) => { await h.click('[data-video="share"]'); await h.pause(800); }},
];

for (const theme of ['light', 'dark']) {
  await record({
    url: `${BASE}/design-preview/video/shelf`,
    out: `shelf-laptop-${theme}`,
    steps,
    viewport: {width: 1280, height: 800},
    dpr: 2,
    context: {timezoneId: 'Europe/Lisbon', locale: 'en-GB'},
    init: async (ctx) => {
      await ctx.addInitScript((t) => localStorage.setItem('theme', t), theme); // a Shipyard app reads its theme from here
      await ctx.clock.install({time: new Date('2026-03-12T10:30:00')}); // "2 minutes ago" reads the same every take
    },
  });
}
```

Helpers: `h.click`, `h.type`, `h.press`, `h.move`, `h.scroll`, `h.focus(target, {zoom})` (where the camera should look, with a ring), `h.unfocus()`, `h.waiting(fn)` (a wait the video speeds through), `h.pause(ms)`, `h.log({type: 'mark', name, box})` (a box the scene can draw on, such as a sentence to highlight). `init(ctx)` sets cookies, `localStorage` and the clock before the page loads. `context` sets the time zone and language so dates read like the story's place.

Record it:

`node "${CLAUDE_PLUGIN_ROOT}/scripts/video-capture.mjs" <appDir> <name> --page /design-preview/video/<page>`

It starts the app on this computer with placeholder keys, waits for the page, runs the capture and always stops the app again. One capture at a time. The recordings (`video/public/capture/`) are too big for GitHub and are not saved there; the capture file is, so anyone can record them again. It prints each take's length and steps. A step that failed is named, and a screenshot of that moment is in `video/out/.capture/<take>/`: open it. An app not built with Next.js: ask the student to start it, then add `--url http://localhost:<port>`.

### Show the real address

Links and address bars in a practice page read `localhost`. To show the real address instead, load the page under it and let the local app answer every request: in `init(ctx)`, `await serveAs(ctx, {origin: 'https://app.example.com', app: BASE})` (import `serveAs` from `./record.mjs`), then record `https://app.example.com/design-preview/video/<page>`. Nothing reaches the real site. The app's dev connection is passed through too; that part needs Node 22 or newer.

### Wide and phone from two takes

Text is readable on a phone only from a tall take. Record the same steps twice (for example 1440 by 900 for the wide cut and 980 by 1150 for the phone cut), log the boxes the camera needs as marks (`h.log({type: 'mark', name: 'panel', box})`), and let the Demo pick the take by `format` and read the boxes from it, so one set of scenes serves both.

### People talking

A client on a call or a team in a meeting: write their lines in `video/capture/specs/<name>.json`:

```json
{"out": "public/call", "lang": "en", "lines": [
  {"clip": "client", "voice": "coral", "text": "Can we see the new menu on Friday?"},
  {"clip": "client", "voice": "ash", "text": "Friday works.", "gap": 0.4}
]}
```

`video-voice.mjs <appDir> --clips video/capture/specs/<name>.json` makes `video/public/call/client.wav` and `clips.json` with the time of every word. Pick clearly different voices for different people. The practice page can type each line word by word at those times; measure how far the page lags the sound on stills for each take and shift the recording by it. Play the clips to the student before they go in.

### The student's own work

Their homepage, a slide, a document: draw it in the scenes rather than recording it. It is their material, not the app's, and it can animate when the app's result lands.

## 4. Build the scenes on the recording

Each scene plays one step of a take with `<Footage>` from `video/src/footage.tsx`:

```tsx
<Footage cap={CAPTURES['shelf-laptop-light']} step="add" width={1600} height={1000} ringColor={K.accent} />
```

- `camera`: shots `{f, box, zoom, ring}` the scene sets itself, instead of the take's focus marks.
- `followY` (phone cut): the page's full width fills the screen and the camera moves up and down to each focus.
- `from` (seconds into the step), `speed` (faster than real time), `lead` (frames before the step starts).
- `overlay(t)`: marks drawn on the app at time `t`, for example a highlighter over a sentence.
- `tap`: a finger tap instead of the arrow cursor (phones).

Waits logged with `h.waiting` play compressed to about 0.8 seconds, and the step's last frame holds. Themes: record both, then swap the takes and the palette in an `apply<Product>(theme)` like rebuilt scenes do. Variants (light and dark, a second angle, a version with prices) are extra scripts on the same Demo, listed in `products.json`. Register the product as in `references/scenes.md`, then `npx tsc --noEmit`.

## 5. Matching a recorded sound

If the page reacts to a sound in the video (a voice clip, a call), the page shows its reaction 0.7 to 1.1 seconds after the sound, and the delay differs per take. Measure it on stills for each take and keep that offset per take name. Check every such moment on the stills: the spoken word and the word on screen must land together.

## 6. Pitfalls that each cost hours

- **Wrong frames in a long recording.** Never swap `Footage` for Remotion's `<Freeze>`: it clamps the frame to the video's own length, so a long take inside a short video shows earlier frames. `Footage` already avoids it.
- **Blurry or jumpy big recordings.** Remotion shows only the keyframes of video above about 8.9 million pixels a frame. The recorder scales bigger takes down and keeps keyframes close together; do not undo that.
- **Captions in another alphabet.** The engine matches spoken words to the script in any alphabet. Custom word matching must keep every letter (`\p{L}` in a regular expression), or every Greek word matches nothing.
- **No browser.** "Executable doesn't exist": run `npx playwright install chromium` in the app folder once. Or set `CHROME_PATH` to a Chromium build that is already on the computer.
- **Out of memory or disk** while rendering a long take: see "Memory and disk" in `references/qa-render.md` (`--low-memory`).
- **Browsers that vanish.** Playwright's downloaded browsers can disappear with a disk clean-up. `video-capture.mjs` then uses a headless shell that is still there. Never full Chrome: its recording covers only its window and comes out stretched.
- **"2x4" turns into "2×4".** The Inter font changes an x between digits. Turn that off on names and addresses that have one: `fontFeatureSettings: '"calt" 0'`.
- **Register before the voice.** A voiced script that no product lists is skipped and cannot be rendered: add it to `products.json` and `products.ts` first.
