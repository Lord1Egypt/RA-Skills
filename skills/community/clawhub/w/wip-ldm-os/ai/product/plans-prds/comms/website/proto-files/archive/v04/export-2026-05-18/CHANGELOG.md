# WIP Computer - May 18, 2026 design changes

Drop these files into the matching paths in their repos. All changes preserve
existing behavior; nothing in the deploy pipeline needs to change.

## Files changed

### `wip-websites-private` repo - wip.computer/

```
wip.computer/index.html      ← footer restructured: 5 columns grouped into 3
wip.computer/styles.css      ← footer column rules; overflow-x clip;
                                products__head padding-right; 1-col mobile
wip.computer/app.js          ← passkeys info popover: viewport-aware
                                positioning, scroll/click-outside dismiss
```

### `wip-ldm-os-private` repo - src/hosted-mcp/

```
src/hosted-mcp/app/kaleidoscope-login.html
  ← background changed from cream (#FFFDF5) to white (#FFFFFF)
  ← desktop `overflow: hidden` removed so the footer can flow below the fold
  ← replaced `<div id="kscope-footer">` + `/app/footer.js` with the homepage
    footer markup (5 columns: AI Infrastructure / AI Skills / Applications /
    Tools / Connect grouped into 3 col-groups; bottom row with copyright +
    legal links)
  ← inlined the footer CSS + JS (passkeys toggle + info popover)
  ← old inline `isLocalPasskeysOn` / `toggleLocalPasskeys` helpers preserved
    so the existing sign-in logic (line ~944) still works; only
    `updatePasskeysDot` was rewritten to target the new `[data-passkeys]`
    and `[data-passkeys-label]` selectors

src/hosted-mcp/legal/privacy/en-ww/index.html
src/hosted-mcp/legal/internet-services/terms/site.html
  ← background changed from cream to white (header bg too)
  ← old `footer { text-align: center }` + `footer span { display: block }`
    removed (they were forcing the new footer columns to render centered
    and breaking inline-flex layouts)
  ← replaced `<div id="kscope-footer">` + `/demo/footer.js` with the
    homepage footer markup (same as above)
  ← inlined the footer CSS + JS
  ← existing sprite icon in the header is untouched and continues to
    render via the inline JS using /demo/sprites.png
```

## Footer column structure

```
WIP Computer, Inc.        AI Infrastructure   AI Skills           Tools
Learning Dreaming         LDM OS              Universal           Are you an AI agent?
  Machines                Memory Crystal        Installer         Local passkeys off (i)
Made in California.       Dream Weaver        1Password
                          Bridge              DevOps Toolbox      Connect
                                              X + xAI             GitHub @wipcomputer
                                                                  X @wipcomputer
                                              Applications
                                              Kaleidoscope
                                              Remote Control
                                              CLVR
                                              Markdown Viewer
```

Grid template: `1fr repeat(3, auto)` at desktop. Brand col gets 1fr; the
3 col-groups (Infrastructure | Skills+Apps | Tools+Connect) each get auto.

Responsive behavior:
- < 960px: tighten gap to 32px (still 4-col on one row)
- < 720px: collapse to a single column. All content stacks in source order.

## Bottom row

```
Copyright © 2026 WIP Computer, Inc. All rights reserved.   Privacy Policy   Terms of Use
```

## Footer JS contracts

- `[data-passkeys]` - button. On click toggles `localStorage.localPasskeys`
  between `'on'` and `'off'`. Adds `.is-on` class when on (turns the dot
  green; off is red). Updates `aria-pressed` and `aria-label`.
- `[data-passkeys-label]` - span inside the button. Text is updated to
  "Local passkeys on" / "Local passkeys off". The label sits inside a
  width-reserving wrapper so the column doesn't shift when toggling.
- `[data-passkeys-info]` - small (i) icon button. Click toggles the
  `aria-expanded` attribute. The popover (sibling `.site-footer__info-popover`)
  reads CSS `--shift` from JS to stay inside the viewport at narrow widths.
  Clicking outside, pressing Escape, scrolling > 24px, or resizing all
  close it.

## Known not-yet-applied

- The `/app/footer.js` and `/demo/footer.js` files themselves are still
  in the repo but no longer referenced by the three updated pages.
  Other pages may still load them - if you want a global change, replace
  the footer-render logic inside those .js files to emit the same markup.
- The privacy and terms pages still have `.container { max-width: 640px }`
  for the legal text body. Only the footer escapes the container and uses
  the homepage's 1040px footer max-width. If you want the legal text to
  also stretch wider, change `.container { max-width }` to something larger.
