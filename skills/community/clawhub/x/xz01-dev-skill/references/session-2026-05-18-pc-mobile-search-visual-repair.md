# Session 2026-05-18 — PC/Mobile Search Visual Repair

## Trigger

User reported on `https://www.900az.com/` and `https://m.900az.com/`:

- PC search box placed in the visual center is ugly and must not be top-center.
- Mobile search should look like a magnifier/small entry, not a large input pinned at the top.

## Durable lesson

For xz01 live-site visual regressions, a search repair is not complete just because the search functionality is disabled. The visual shape and placement must also match the user's acceptance target:

- PC: search may remain in the top/header area only if it is clearly right-aligned/side-aligned and visually weakened; it must not occupy the header/page center or appear as a dominant large input.
- Mobile: replace any full-width or large top input with a compact magnifier-like visual-only entry, ideally a small round/icon button near the logo/top controls.
- Search must stay visual-only unless explicitly requested otherwise: no `/search` action/link, no enabled input, no submit button, and no JS submit binding.

## Verification pattern

1. Apply the smallest theme-only patch under `public/themes/<theme>/**`; do not touch PHP/backend/controller/model/config/route files.
2. Clear `/www/wwwroot/www.900az.com/runtime/` after every add/modify/delete.
3. Run independent visual validation with:
   - PC wide screenshot of `https://www.900az.com/`.
   - Mobile-domain screenshot of `https://m.900az.com/` using a real mobile UA and ~390px viewport.
4. AI/vision checks must explicitly answer:
   - PC: is search top-center or dominant?
   - Mobile: is there a visible small magnifier/search entry, and is it not a large top input?
   - Mobile: are first-screen card grids clipped or horizontally overflowing?
5. If test says "large input removed but magnifier not visible," treat it as a failed/partial fix and immediately do a second precise dev pass; do not report success.

## Concrete implementation notes from this session

- PC repair used CSS to move the existing disabled search visual to the right and shrink/soften it.
- Mobile repair changed the header DOM from input+button to inert spans and used CSS `:before`/`:after` to draw a magnifier.
- A second pass was needed because the first mobile version made the search entry too subtle; final acceptance used an obvious ~38px white circular icon.
- Mobile overflow guards were added around 390px: `box-sizing:border-box`, `max-width:100%`, `min-width:0`, and overflow clipping for card grids/items.

## Pitfall

Do not equate "not a big input" with "passed." The user explicitly expects a magnifier/small search-entry visual on mobile. If the icon is absent or too subtle to see in the screenshot, continue fixing.