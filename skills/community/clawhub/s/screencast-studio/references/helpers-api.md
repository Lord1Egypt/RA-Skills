# Helpers API

The five helpers exposed inside the `try { ... }` block of `record.js`. All are async unless noted.

## `await sub(label)`

Adds a subtitle event to the events log and holds the page for a duration scaled by character count.

```js
await sub('Bottom of overview — recent activity, scheduled tasks');
```

**Hold time formula**:
- 700ms base
- + 130ms per CJK character
- + 55ms per ASCII character
- + 30ms per whitespace
- clamped to `[1100, 3500]` ms

So a short English subtitle holds for ~1.1s; a 30-character Chinese subtitle holds for ~3.5s. This is "comfortable reading speed" calibrated empirically. If you need a longer hold (e.g. while a complex UI animates in), pair `sub()` with explicit `hold(ms)`:

```js
await sub('Settings page loading...');
await hold(2000); // give it more time on top
```

## `await click(locator, label)`

The full click ceremony. In sequence:

1. **Scroll target into view** if needed (`scrollIntoViewIfNeeded`) + 150ms settle
2. **Get bounding box center** of the locator
3. **Push a `move` event** at that position to `events.json`
4. **Pause 700ms** (`PAUSE_BEFORE_CLICK`) — cursor visibly arrives + dwells
5. **Push a `click` event** at the same position
6. **Trigger the actual click** via `locator.click()`
7. **Pause 500ms** (`PAUSE_AFTER_CLICK`) — ripple + UI reaction stay on screen

```js
const filesTab = page.locator(':is(button, a, [role="tab"])').filter({ hasText: /^\s*Files\s*$/ }).first();
await click(filesTab, 'Switch to Files tab');
```

The `label` becomes a video event annotation (visible in `events.json` and `review/flow/report.txt`).

### Tuning the dwell times

If the UI animates slowly and the cursor is "rushing" the user, increase `PAUSE_BEFORE_CLICK` / `PAUSE_AFTER_CLICK` constants near the top of `record.js`. 700/500 is the default that survived a real demo with ~22 clicks.

### When click fails

If the click throws "bounding box missing", the locator didn't resolve to a visible element. Check:

1. Is the element actually rendered? (Some UI lazy-loads on hover.)
2. Did a previous step navigate away? (Re-find the locator.)
3. Is the selector ambiguous? (Use `.first()` or `getByText(s, { exact: true })`.)

Wrap with `tryStep` if the click is genuinely optional.

## `await scroll(deltaY, ticks=1)`

Wheel-scrolls the main content area.

```js
await scroll(400, 2);  // scroll down 800px total, in 2 wheel ticks with 280ms between
```

- `deltaY` positive = scroll down, negative = scroll up
- `ticks` = how many wheel events to dispatch (more = smoother)

**Important**: this helper first parks the mouse at the **center of the viewport** (`mouse.move(VIEWPORT.width/2, VIEWPORT.height/2)`) so the wheel event lands on main content, not the sidebar. If you call `page.mouse.wheel` directly, the cursor's "logical position" defaults to (0, 0) and the wheel scrolls whatever's there — typically the sidebar — which usually isn't what you want.

If your app has multiple scrollable containers in the main area, `scroll()` may still hit the wrong one. In that case, escape to:

```js
await page.locator('[data-testid="task-list"]').evaluate((el, dy) => el.scrollBy(0, dy), 400);
```

## `hold(ms=400)`

Plain pause. Returns a promise; `await` it.

```js
await hold();      // 400ms default
await hold(1500);  // 1.5s
```

Use to:
- Let an animation finish before the next click
- Hold a settled state on screen while subtitle reads

## `await tryStep(name, fn)`

Wraps a sub-flow in try/catch + logs. If `fn` throws, the error is caught and logged as `✗ ${name} — skipped: <message>`, then execution continues.

```js
await tryStep('Open detail panel', async () => {
  const openBtn = page.locator('button').filter({ hasText: /Open Details/i }).first();
  await openBtn.waitFor({ state: 'visible', timeout: 4000 });
  await click(openBtn, 'Click "Open Details"');
  await sub('Detail panel — structured fields and sections');
  await hold(1500);
  // ... close + cleanup
});
```

**When to use `tryStep`**:
- Optional UI surface (depends on user permissions / data state)
- Stage that might be removed or renamed in the target app
- Anything where "skip on failure" is acceptable

**When NOT to use `tryStep`**:
- Required stages — if they fail, you want the recording to abort so you don't ship a broken demo
- Login / setup
- The first navigation (if it fails, nothing else will work)

## Persistent masks (CONFIG, not a helper)

Configured in `record.js` top-level CONFIG block, NOT inside the stage flow:

```js
const PERSISTENT_MASKS = [
  { selector: '.user-badge',  label: 'username' },
  { selector: 'header .logo', label: 'logo' },
  { box: { x: 0, y: 820, w: 220, h: 80 }, label: 'sidebar-bottom' },
];
```

Resolved automatically by `record.js` immediately after first navigation — before your STAGE FLOW runs. Each mask becomes a `mask_persistent` event in `events.json`; `postprocess.js` then crops + boxblurs the region and overlays it back at the original coordinates as the final composition layer (above subtitles + cursor + ripples).

### When to use selector vs box

**Selector** (`{ selector: '...', label: '...' }`):
- Use when the element is `position: fixed` or `position: sticky` — boundingBox stays consistent through the entire video
- record.js queries `getComputedStyle(el).position` after resolving; warns in the log if not fixed/sticky

**Box** (`{ box: {x, y, w, h}, label: '...' }`):
- Use when selector is unreliable, or you've measured coordinates from a `review/sensitive/scan-XX.png` after ship and need to retroactively cover a region
- `box` masks don't require re-recording — edit `PERSISTENT_MASKS`, run `npm run render && npm run review:sensitive`. The original `events.json` is kept and re-used.

### Tuning the blur

`postprocess.js` uses `boxblur=lr=20:lp=2:cr=15:cp=2`. The `lr` / `lp` are luma radius / iterations; `cr` / `cp` are chroma radius / iterations. Chroma is split out because ffmpeg caps chroma radius at 15 — `boxblur=20:2` (which would set both to 20) would error. Tweak in `postprocess.js` filter chain if:
- Text inside the masked region is still readable → increase luma radius (try `lr=40:lp=2:cr=15:cp=2` or `lr=60:lp=3:cr=15:cp=3`)
- Mask looks "pixelated" instead of smooth → increase iterations (`lr=20:lp=3:cr=15:cp=3` or `lp=4:cp=4`)

## Escape hatches

The helpers cover the common 80%. For anything else, the underlying Playwright `page` is in scope:

```js
// Direct keyboard
await page.keyboard.press('Escape');

// Dialog handling
page.on('dialog', (d) => d.accept());

// Custom waits
await page.waitForFunction(() => window._myFlag === true, { timeout: 5000 });

// File upload
const fcp = page.waitForEvent('filechooser');
await click(uploadBtn, 'Click upload');
const fc = await fcp;
await fc.setFiles(['/path/to/file.png']);
```

When you use `page.something()` directly, **no events are recorded** — the synthetic cursor won't move, the click ripple won't fire. That's usually fine for keyboard / dialog / file-chooser steps, but means you can't use raw `locator.click()` if you want it to appear in the cursor track. Always go through `click(locator, label)` for visible interactions.

## What lives in `events.json`

Every helper / config that affects video output pushes events:

| Source | Pushes |
|---|---|
| `sub(label)` | `{ t, kind: "subtitle", label }` |
| `click(...)` | `{ t, kind: "move", x, y }` then `{ t, kind: "click", x, y, label }` |
| `scroll(...)` | (no events — just causes UI to scroll) |
| `hold(...)` | (no events — pure timing) |
| `tryStep(...)` | (no events — wraps fn) |
| `PERSISTENT_MASKS` (CONFIG) | one `{ t: 0, kind: "mask_persistent", x, y, w, h, label }` per resolved entry |

See [events-schema.md](events-schema.md) for the full schema and how postprocess consumes it.
