# SendPulse Marketplace UI — project rules for Gemini

> Copy this file into your project root as `GEMINI.md` (or merge into an existing one). Keep the
> skill folder in the repo — paths below assume `docs/sendpulse-marketplace-ui-cdn/`; adjust if you
> cloned it elsewhere. For a **Gemini gem** (no repo, no shell) use
> `adapters/chatgpt/instructions.md` as the gem instructions and attach the files it lists instead.

When the task is UI inside a SendPulse marketplace integration — a settings or connection screen, a
widget, an embedded page, dark theme, panels rendering transparent, forms, buttons, modals, tables,
dropdowns, badges, `sp_icons`, colour tokens or layout inside the host iframe — read
`docs/sendpulse-marketplace-ui-cdn/SKILL.md` first and follow it. Detailed references:

- `references/components.md` — the component catalogue: every load-bearing class with its markup
- `references/gaps.md` — sixteen classes that look like they work and don't: symptom → cause → fix
- `references/classes.txt` · `references/icons.txt` — 1411 class names, 536 icon names; grep, don't guess
- `references/tokens.css` — the 28 custom properties the bundle reads and never defines
- `references/bundle-fixes.css` — the structural gaps as copy-paste CSS
- `references/tokens.md` — the light palette, for when no semantic class covers the case
- `references/starter.html` — the correct `<head>`: both theme builds, load order, theme switch
- `references/kitchen-sink.html` — every component rendered correctly; copy markup from here
- `examples/settings-screen.html` · `examples/amazon-connections-screen.html` — whole screens
- `references/check-build.sh` · `check-classes.sh` · `verify.mjs` — the checkers (Step 7)

Hard rules (apply even without reading the references):

1. Link `https://cdn.sendpulse.com/dist/css/sp-marketplace-app-ui.min.css` ahead of app CSS; never
   vendor a copy — icon fonts resolve against the stylesheet's origin.
2. Load order is the contract: CDN bundle → `tokens.css` → `bundle-fixes.css` → app CSS last.
3. Only use classes that appear in `classes.txt` (icons: `icons.txt`). Grep before writing a name.
   No re-implemented components, no competing `font-family`, no second icon set.
4. The bundle reads 28 custom properties and defines none — copy `references/tokens.css` verbatim;
   those 28 names are the only ones app CSS may reference.
5. The app fills the host iframe: no padding, no `max-width`, no `margin: 0 auto` and no `overflow`
   on the app root. Cap individual controls at 364px (420/540 by exception) one level in.
6. Dark theme arrives as `?theme=dark` from the host — read it at boot, mirror it as `ma-dark` on
   `<html>`, carry the param through every URL the app builds. Never ship a theme switcher.
7. Paint `body` yourself and declare `color-scheme` for both themes; neither build does.
8. The CDN ships no JS: `.modal`, `.dropdown-menu`, `.collapse`, tabs and tooltips are styling only.
9. Restraint: no decorative icons, one primary button per view, one signal per state, no panel
   inside a panel, empty states text-first.
10. Run `references/check-build.sh` and `references/check-classes.sh` before delivering; add
    `references/verify.mjs` where Node is available. When the live bundle and the skill disagree,
    the bundle wins — `references/refresh.sh` is how you find out.
