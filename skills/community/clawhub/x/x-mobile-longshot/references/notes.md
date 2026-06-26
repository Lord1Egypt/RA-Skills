# x-mobile-longshot notes

## Goal
Produce a mobile-looking long screenshot and optional single-page PDF for X article / long-post URLs.

## Why this exists
Direct `fullPage` screenshots of X mobile pages often include unstable overlays:
- top app-open modal / dialog
- bottom sticky CTA (`在 X 上查看更多` / `获取应用`)
- occasional close/ignore buttons that only respond to DOM-side click

## v1 strategy
1. Open the X URL in Playwright with a mobile device preset and dark mode.
2. Wait for content to render.
3. Click `忽略` / `Close` via in-page DOM execution when present.
4. Remove common overlay nodes by matching fixed/sticky/dialog blocks with X app CTA text.
5. Capture one `fullPage` PNG as the base image.
6. Re-open the URL, repeat the cleanup, capture one clean viewport image.
7. Replace the top portion of the long screenshot with the clean viewport image to remove the top popup region more reliably.
8. Optionally convert the final PNG into a single-page PDF using Pillow.

## Known limitations
- This is a pragmatic capture pipeline, not a perfect native-app emulator.
- Very long pages can still be sensitive to X DOM changes.
- The bottom CTA can reappear if X changes its DOM/text; update the overlay text patterns when needed.
- Telegram may reject extremely tall PNGs as photos; send them as files/zip or PDF.

## Suggested next iteration
If v1 is not clean enough, switch the primary path to segmented viewport capture + stitching. That is more work but should be more robust against sticky/fixed overlays.
