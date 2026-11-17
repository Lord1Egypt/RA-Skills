# Gaps the bundle leaves you — symptom, cause, fix

The diagnostic catalogue SKILL.md Step 6 points at. Every entry here was hit while building against
the live CDN (2026-08-20, causes re-measured in Chrome 2026-08-25) and cost time to diagnose, because the class exists and looks like it
should work. **Find the class you are fighting below and read that entry before concluding you've
used it wrong.** One `##` heading per gap, named after the class, so `grep` and a table of contents
both land you in the right place.

`bundle-fixes.css` · `tokens.css` marks the seven that are already written for you: copy those two
files (Step 0) and those seven stop happening. They stay documented because you still need to
recognise the symptom if you meet it in a repo that didn't copy them. The other nine are decisions,
and this is where they are argued out.

| The class | The symptom | |
|---|---|---|
| [the 28 custom properties](#the-28-undefined-custom-properties) | `.side-panel` transparent, focus rings gone | `tokens.css` |
| [`color-scheme`](#color-scheme--native-select-popup-and-scrollbars-stay-light-in-dark) | native `<select>` popup stays light in dark | `tokens.css` |
| [`.nav-tabs`](#nav-tabs--renders-as-a-bulleted-vertical-list) | renders as a bulleted vertical list | `bundle-fixes.css` |
| [`.badge-status-*`](#badge-status---inside-a-list-group-item-the-dot-is-grey-not-green-or-red) | the dot is grey inside a `.list-group-item` | `bundle-fixes.css` |
| [`.input-group`](#input-group--a-number-and-its-unit-select-sit-far-apart) | number and unit `<select>` sit far apart | `bundle-fixes.css` |
| [`.badge-paid`](#badge-paid--sits-too-low-beside-a-label) | sits too low beside a label | `bundle-fixes.css` |
| [`.avatar`](#avatar--hangs-below-the-labels-baseline-in-a-dropdown) | hangs below the label's baseline | `bundle-fixes.css` |
| [`.sp-icon`](#sp-icon--the-glyph-and-its-label-touch) | glyph and label touch | |
| [`.badge-status`](#badge-status--text-put-inside-it-overflows) | text inside it overflows | |
| [`.list-divided`](#list-divided--shows-bullets) | shows bullets | |
| [`.modal`](#modal--invisible-or-opens-with-no-backdrop) | invisible, or no backdrop | |
| [`.accordion`](#accordion--does-nothing) | does nothing | |
| [`.tab-content`](#tab-content--the-tab-panel-is-unstyled) | the tab panel is unstyled | |
| [`.bootstrap-select`](#bootstrap-select--no-width-caret-unpositioned-native-select-still-visible) | no width, caret unpositioned, native `<select>` still visible | |
| [`.settings-toggle-radius`](#settings-toggle-radius--the-knob-sits-over-the-label) | knob sits over the label | |
| [`.settings-toggle-btn-sm`](#settings-toggle-btn-sm--the-knob-is-on-the-wrong-side) | knob on the wrong side | |

---

## The 28 undefined custom properties

**Symptom.** `.side-panel` transparent, focus rings missing.

**Cause.** The 28 custom properties the bundle references and never defines — they live in
`template.min.css`, which the marketplace bundle does not include (Step 0).

**Fix.** Ship a `:root` / `:root.ma-dark` block lifted from `template.min.css?force=…`. Already
written: copy `references/tokens.css`.

## `color-scheme` — native `<select>` popup and scrollbars stay light in dark

**Cause.** No `color-scheme` in **any** SendPulse stylesheet — 0 occurrences across the marketplace
bundle, `bootstrap.min.css` and `template.min.css`, both themes.

**Fix.** Two declarations on `:root` (SKILL.md Step 5). This is the only thing wrong with a native
select. Already written: copy `references/tokens.css`.

## `.nav-tabs` — renders as a bulleted vertical list

**Cause.** The bundle styles `.nav-tabs > li > a` in detail but drops Bootstrap 3's base `.nav`
rules. `bootstrap.min.css` has them (`.nav{margin-bottom:0;padding-left:0;list-style:none}`); the
marketplace bundle is where they went missing.

**Fix.** Add the four missing `.nav` / `.nav > li` / `.nav > li > a` rules; every visual property
still comes from the bundle. Already written: copy `references/bundle-fixes.css`.

## `.badge-status-*` — inside a `.list-group-item` the dot is grey, not green or red

**Cause.** `.list-group-item .badge{background-color:rgba(70,81,82,.8)}` out-specifies the
single-class `.badge-status-*` modifiers.

**Fix.** Restate the bundle's own colour under `.list-group-item`; leave the modifier off when you
actually want the muted dot. Already written: copy `references/bundle-fixes.css`.

## `.input-group` — a number and its unit `<select>` sit far apart

…and the select is collapsed to its caret.

**Cause.** Not a missing rule — both halves of the table layout are present and correct. Measured in
Chrome against the live build:

- `.input-group{display:table;border-collapse:separate}` **is** there, at top level, and it wins
  (the group computes `display: table`).
- `.input-group .form-control,.input-group-addon,.input-group-btn{display:table-cell}` **is** there
  too, and it works — on a `<div>`.

It fails on the two children that matter. **Chrome refuses `display:table-cell` on `<input>` and
`<select>`**, computing `inline-block` instead, so the table has no cells to lay out. On top of that
the bundle's own `.input-group .form-control{float:left;width:100%}` floats each control at the full
width of the group — and a float blockifies whatever `display` it is given. The two controls end up
as full-width floated blocks, one under the other.

So there is nothing to restore: the table route cannot work with form controls in it, whatever the
CSS says.

**Fix.** Lay that group out as a flex row (`display:flex;width:auto`), size the two children with
selectors specific enough to beat `.input-group .form-control{width:100%}`, and let the bundle's
`:first-child` / `:last-child` rules flatten the inner corners — a `gap` is wrong, the pair is one
control. Already written in `references/bundle-fixes.css`, but **this is the one fix there that also
needs markup**: `.input-group-fit` on the group plus `.input-group-number` / `.input-group-unit` on
the children.

## `.badge-paid` — sits too low beside a label

Beside a form label, or beside the bold title of a `.switcher-flex-holder` row.

**Cause.** `vertical-align:sub`, plus `top:-2px` on `.badge-paid-sm` — sized for a button's caps,
not 16px label text.

**Fix.** `vertical-align:middle;top:0` scoped to those labels. Already written: copy
`references/bundle-fixes.css`, which covers all three sizes.

## `.avatar` — hangs below the label's baseline in a dropdown

In a dropdown trigger or a menu row.

**Cause.** `.avatar` is `inline-block` with no `vertical-align`.

**Fix.** `vertical-align:middle` on `.dropdown-toggle > .avatar` and `.dropdown-menu .avatar`.
Already written: copy `references/bundle-fixes.css`.

## `.sp-icon` — the glyph and its label touch

**Cause.** `.sp-icon` has no margin outside `.btn` / `.dropdown-menu` (Step 3).

**Fix.** `.margin-right-5`. Better still, check the glyph earns its place at all — *Restraint*,
Step 2.

## `.badge-status` — text put inside it overflows

**Cause.** It is a 10×10px dot (`components.md`).

**Fix.** Dot plus a sibling label.

## `.list-divided` — shows bullets

**Cause.** It never resets `list-style` (`components.md`).

**Fix.** Add `.list-unstyled`.

## `.modal` — invisible, or opens with no backdrop

…and the page scrolls behind it.

**Cause.** `.modal{display:none}` and only `.in` animates the dialog; the bundle ships no JS
(non-negotiable #5) and no backdrop element.

**Fix.** Set `display:block` + `.in` yourself, render your own `.modal-backdrop.fade.in`, add
`modal-open` to `<body>`, wire Escape and the backdrop click.

## `.accordion` — does nothing

**Cause.** The class exists but only sets `width`.

**Fix.** Build it from `.panel-group` + `.collapse` / `.in`.

## `.tab-content` — the tab panel is unstyled

**Cause.** Tabs are styled; there is no generic `.tab-content`.

**Fix.** Style the panel yourself.

## `.bootstrap-select` — no width, caret unpositioned, native `<select>` still visible

**Cause.** The plugin's own CSS is a separate vendor file that no SendPulse stylesheet contains —
`bootstrap.min.css` skins it too and also has no `.bootstrap-select{}` base. So the bundle carries
the skin and none of the structure: no `.bootstrap-select{width}`, no
`.bootstrap-select > select{position:absolute;width:.5px;opacity:0}`, and the caret rule assumes a
`position:absolute` never set.

**Fix — first ask whether you need it.** For an avatar/label row, `.form-control.dropdown-toggle` is
fully styled by the bundle and needs no plugin (`components.md`, *Forms*). If you do need search or
groups: keep the real `<select>` in the wrapper as the value carrier and hide it with the bundle's
`.sr-only`; take layout from `.d-block` / `.clearfix` and a flex `.dropdown-toggle`. The wrapper's
own `position:relative` comes free from `.btn-group`.

## `.settings-toggle-radius` — the knob sits **over** the label

**Cause.** The only rules that position it are descendant selectors.

**Fix.** Nest it *inside* each label span, not as a sibling.

## `.settings-toggle-btn-sm` — the knob is on the wrong side

**Cause.** Internally inconsistent in the bundle: inactive padding reserves 25px on the right, while
`.settings-toggle-off .settings-toggle-radius` puts the knob left.

**Fix.** Not fixable app-side — use the default size.

---

## Three that are not bugs and must not be "fixed"

- **Root-relative asset URLs.** `url(/my.fonts/…)` and ~50 `url(/img/…)` references resolve against
  the **stylesheet's** origin, so they land on `cdn.sendpulse.com` and work from any host. This is
  precisely why vendoring the stylesheet breaks them (non-negotiable #1).
- **No gap scale beyond `.gap-5`**, and the numeric `.margin-*` / `.padding-*` set is sparse. Check
  `references/classes.txt` before using one; most numbers are not defined.
- **A `<select>` popup that opens detached from its control is DevTools, not CSS.** Chrome's device
  emulation does not reposition OS-drawn popups — select dropdowns, date pickers and autofill are
  separate windows placed at real browser-window coordinates, while the emulated page is a scaled,
  offset rectangle inside it. Nothing in a stylesheet can move them. Verify small screens by
  resizing the actual window, not with device mode.
