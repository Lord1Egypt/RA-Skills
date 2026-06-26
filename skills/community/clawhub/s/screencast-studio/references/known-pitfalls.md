# Known pitfalls

Every category of bug encountered when authoring + shipping screencasts with this skill, with how to avoid each. Read this before declaring a recording done.

## Cursor off-frame

**Symptom**: in the final video, cursor flies off the bottom (or right) of the screen during a click, ripple flashes off-screen, then UI suddenly reacts.

**Cause**: `boundingBox()` returns viewport-relative coordinates *at the time of the call*. If the click target is below the viewport, `box.y` will be greater than the viewport height. Playwright's `locator.click()` will scroll to bring the target into view, but the synthetic cursor was already told to fly to `(x, y)` outside the recorded frame.

**Fix**: the `click` helper already does `scrollIntoViewIfNeeded` + 150ms settle before reading the bounding box. **Always use `click(locator, label)` for visible interactions** — never bypass with raw `locator.click()`.

**Detect**: in `events.json`, look for click events with `y > viewport.height - 100`. After every ship, scan `review/flow/click-XX-A-pre.png` for any frame where the cursor isn't visible.

## Wheel scrolls the wrong container

**Symptom**: subtitle says "scroll to see X" but UI doesn't visibly scroll. `review/visual/sub-XX.png` looks identical to the previous stage.

**Cause**: `page.mouse.wheel(0, dy)` dispatches a wheel event at the mouse's *logical position*, which defaults to (0, 0) — typically inside the sidebar. The sidebar scrolls (sometimes nothing happens because the sidebar doesn't overflow), and the user sees no change in the main content.

**Fix**: the `scroll(deltaY, ticks)` helper parks the mouse at viewport center first. **Use the helper, not `page.mouse.wheel` directly**.

**When the helper isn't enough**: if the main area has multiple nested scroll containers, viewport center may land on the wrong one. Escape to:

```js
await page.locator('[data-testid="task-list"]').evaluate((el, dy) => el.scrollBy(0, dy), 400);
```

## Substring-match selector ambiguity

**Symptom**: cursor flies to an element that's clearly not the labeled target. Ripple fires on the wrong row.

**Cause**: `page.locator('text=..')` matches any element whose `textContent` *contains* `..`. So `text=Save` matches "Save", "Saved", "Save changes", "Unsave". `text=..` (literal two periods) matches nearly everything because most text contains 2+ characters.

**Fix**: use exact match for short / generic labels:

```js
page.getByText('Save', { exact: true })
page.getByText('..', { exact: true })  // ✓ matches only the literal ".."
page.locator(':is(button, a)').filter({ hasText: /^\s*Save\s*$/ }).first()  // ✓ regex pin
```

For `text=` with a regex, use `^...$` anchors:

```js
page.locator('text=/^Save$/')
```

## tryStep silently swallows failures

**Symptom**: ship succeeds with no errors. But `review/coverage/stage-XX.png` for some stage shows no UI change — the entire stage didn't execute.

**Cause**: `tryStep('name', async () => { ... })` catches any exception inside the function and logs `✗ name — skipped: ...` to stdout. If you don't watch stdout, the failure is invisible.

**Fix**:
1. **Read `npm run record` stdout** — every `✗` line is a stage that silently skipped.
2. **Only wrap genuinely optional stages in `tryStep`**. Required stages should throw and abort the recording.
3. **Sample `review/coverage/stage-XX.png`** for any stage you wrapped in `tryStep` — if the screenshot looks like a previous stage's UI, the wrapped stage skipped.

## Stale UI in pre-click frame

**Symptom**: `review/flow/click-XX-A-pre.png` shows the *next* stage's UI, not the current one. Cursor is on a button that exists in the next view, not the current view.

**Cause**: `review.js` samples A-pre at `t - 0.20s`. If the previous click triggered an immediate UI transition (e.g. opening a modal that blocks the previous view), the 200ms window can fall inside the transition period, and the screenshot reflects the post-transition state. Cursor was correctly placed at the click time, but the visible UI has moved on.

**Fix**: this is mostly cosmetic — the click itself is correct, just the review screenshot is misleading. If it bothers you:
- Increase `PAUSE_AFTER_CLICK` in `record.js` so the previous UI lingers longer
- Or accept it: the B-mid (`t + 0.05s`) and C-react (`t + 0.35s`) screenshots will still tell the real story

## Subtitle and UI mismatch

**Symptom**: `review/visual/sub-XX.png` shows a UI state that doesn't match the subtitle text. E.g. subtitle says "8 tasks in progress" but UI shows "23 tasks".

**Cause**: the subtitle was authored against an assumed state; the actual state when the recording ran was different. Common reasons:
- Test data drift (the project no longer has 8 tasks; it has 23)
- Subtitle copy-paste from an older version
- Subtitle describes intent rather than state ("here we see X" when X isn't actually visible)

**Fix**: only the author can fix. Audit every `sub('...')` call against what the UI actually shows in `review/visual/`. Subtitles should describe what's on screen, not what *should be* on screen.

## CJK characters render as boxes

**Symptom**: subtitles show ▢▢▢▢ instead of Chinese / Japanese / Korean.

**Cause**: postprocess picks a font name based on `process.platform`, but the picked font isn't installed.

**Fix**:
- **Linux**: `apt install fonts-noto-cjk` (Debian/Ubuntu) / `dnf install google-noto-cjk-fonts` (Fedora) / equivalent
- **Override**: `SUBTITLE_FONT="<an installed font name>" npm run render`
- **Verify**: list installed fonts with `fc-list` (Linux/macOS); look for one with CJK glyphs

## "events.json missing" / "raw.webm missing"

**Symptom**: `npm run render` or `npm run review` fails with these errors.

**Cause**: `record.js` didn't complete successfully (e.g. login failed, `STAGE FLOW` placeholder error not yet replaced).

**Fix**:
- Run `npm run record` separately and watch for the actual error
- Verify `storageState.json` exists (run `npm run login` if not)
- Verify the `STAGE FLOW` block in `record.js` has been replaced with real flow (the template throws "No stage flow defined yet" by default)

## ffmpeg crashes mid-render

**Symptom**: `npm run render` hangs or exits with non-zero status.

**Cause**: usually one of:
- `events.json` has a click event with NaN / undefined coordinates (e.g. boundingBox returned null and we didn't catch it)
- Filter graph too long (uncommon — needs hundreds of clicks)
- libass error parsing subtitle file (look for invalid ASS escape sequences in subtitle text)

**Debug**:
```bash
cat events.json | jq '.[] | select(.x == null or .y == null)'  # find malformed events
```

## Subtitle count ≠ recording correctness

**Symptom**: `npm run ship` finishes, says "✓ visual 25 subtitles → 25 frames", you mark complete, user finds 8 obvious problems on first watch.

**Cause**: the report.txt and subtitle counts only prove that the events fired and ffmpeg didn't crash. They prove nothing about whether the demo *looks correct*.

**Fix**: after every `npm run ship`, **read the review screenshots**:

1. **Read every `review/visual/sub-XX.png`** — does subtitle match UI?
2. **Sample `review/flow/click-XX-A-pre.png`** for clicks with high `y` or large delta from prev click — is cursor on target?
3. **Sample `review/coverage/stage-XX.png`** for any `tryStep` stage — did it actually execute?
4. **Read every `review/sensitive/mask-XX-*.png` and `scan-XX-*.png`** — masks blurred enough? Any PII visible in the unmasked frame scans?

If you find issues, fix `record.js` (or just add box masks for the sensitive pass), re-ship (or `npm run render && npm run review:sensitive` for mask-only iterations), re-read. The cycle ends only when all 4 passes (flow / visual / coverage / sensitive) look right.

## Mask region drifts off the masked element

**Symptom**: in `review/sensitive/scan-XX.png`, you see the blurred rectangle is no longer covering its intended target — the element has moved (e.g. user scrolled and the masked element scrolled with the page) and the mask sits over empty space, exposing what it was supposed to hide.

**Cause**: `selector`-based persistent masks capture `boundingBox()` once at the start of recording. If the element is `position: static` / `relative` / `absolute` (i.e. part of normal flow), it moves when the page scrolls, but the captured (x, y, w, h) is locked.

**Fix**:
- **Prefer fixed-positioned elements** for selector masks. The resolver in `record.js` warns when an element's computed `position` is not `fixed` or `sticky` — heed that warning.
- **Switch to a `box` mask** that covers the worst-case viewport position. Often simpler than fighting CSS:
  ```js
  // before: { selector: '.user-info', label: 'username' }
  // after:  { box: { x: 0, y: 800, w: 240, h: 100 }, label: 'sidebar-bottom' }
  ```
- **No selector tricks fix this** — even with re-querying, recording is sequential and the mask is one-shot at startup. Dynamic-following masks are not in v0.2.

## Mask blur is too weak — text still readable

**Symptom**: in `review/sensitive/mask-XX-*.png`, you can squint and read the text inside the blurred region (especially for large/bold/high-contrast text).

**Cause**: the default `boxblur=lr=20:lp=2:cr=15:cp=2` is tuned for typical SPA chrome (badges, footers, small text). High-contrast / large-font content benefits from more aggressive blur.

**Fix**: edit `postprocess.js`, find the `boxblur=...` in the persistent-mask block, and try one of:
- `boxblur=lr=40:lp=2:cr=15:cp=2` — wider luma kernel (more smearing horizontally + vertically). Chroma stays capped at 15 (ffmpeg constraint).
- `boxblur=lr=20:lp=4:cr=15:cp=4` — more iterations (smoother gaussian-like falloff)
- `boxblur=lr=60:lp=3:cr=15:cp=3` — both, for stubbornly readable text
- Replace with `pixelize=20:20` for unmistakable mosaic blocks (block size 20×20)
- `gblur=sigma=15` — proper Gaussian, no chroma cap, slightly slower

Re-render with `npm run render`, re-check `review/sensitive/`. No re-record needed.

## Sensitive scan shows PII not covered by any mask

**Symptom**: `review/sensitive/scan-XX-tNNs.png` reveals a username, version number, internal codename, or business strategy text that's visible in the recording but not inside any current `PERSISTENT_MASKS` region.

**Cause**: missed during the upfront mask configuration round. Often it's content that only appears mid-flow (e.g. a project name shown after navigating into a detail view).

**Fix**: NO need to re-record. Add a `box` mask:
1. Open the offending `scan-XX-tNNs.png` and measure the rectangle in pixel coordinates (most image viewers show cursor coords; or open in any editor that displays them)
2. Add to `PERSISTENT_MASKS`:
   ```js
   { box: { x: 320, y: 180, w: 600, h: 90 }, label: 'project-title-bar' }
   ```
3. Run `npm run render && npm run review:sensitive`
4. Repeat until `review/sensitive/` is clean

## "Why does my video look 1080p but the recording was 1440x900?"

This is a Read-tool artifact, not a real video issue. The `Read` tool downscales large images for display. The actual `final.mp4` is whatever resolution Playwright recorded at (default 1440×900). Verify with:

```bash
ffprobe final.mp4 2>&1 | grep Stream
```

Should report `1440x900` or whatever you set `VIEWPORT` to.
