---
name: sendpulse-marketplace-ui-cdn
description: >
  UI work in a SendPulse marketplace integration that links the prebuilt
  `sp-marketplace-app-ui.min.css` from the CDN — app, embedded widget or standalone page, any
  framework or none. Building a settings or connection screen, fixing dark theme, or panels
  rendering transparent with focus rings missing. Forms, buttons, modals, tables, dropdowns, badges,
  `sp_icons`, colour tokens, layout utilities, `?theme=dark` / `ma-dark` light and dark builds,
  layout inside the host iframe.
version: 1.1.0
license: MIT
metadata:
  author: SendPulse
  homepage: https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-marketplace-ui-cdn
---

# SendPulse Marketplace UI kit — the CDN bundle

**Be simple.** When two options both work, ship the one with fewer elements, fewer classes and
fewer glyphs. SendPulse screens are deliberately plain; the shortest correct markup is the house
style, not a shortcut. Two consequences, each stated in full where it applies: one `.panel` flush to
the frame does the screen layout (Step 4), and nothing is added that carries no information (Step 2,
*Restraint*). Nothing here needs a second skill to be usable.

**Scope: the CDN stylesheet.** Everything about wiring here — Step 0's `<link>` and load order,
the custom properties Step 1 has you ship, the two theme builds of Step 5 — assumes the app gets
the design system from

```
https://cdn.sendpulse.com/dist/css/sp-marketplace-app-ui.min.css
```

If the app you are working in already receives the design system some other way, through its own
build pipeline rather than that URL, then it also has its own `:root`, its own asset paths and its
own theming switch, and applying Step 0, Step 1 or Step 5 there will fight what is already set up.
Leave that wiring alone and ask whoever set the repo up. **Steps 2–4 still hold either way** — the
class vocabulary, the icons, the layout rules and the restraint rules are the design system itself,
not the delivery method.

**Without a filesystem or a shell** — a chat window rather than an agent — Steps 0–5 still hold in
full; Step 6 needs `references/gaps.md` pasted in; Step 7 becomes the manual checklist in
`adapters/chatgpt/pocket-guide.md`. That file and `adapters/chatgpt/instructions.md` are the
condensed, self-contained form of this skill for tools that cannot open files; `adapters/README.md`
covers installing it in ChatGPT, Gemini, Cursor and Copilot.

> **Non-negotiables — read before writing markup.** Each is spelled out in the step named.
>
> 1. **Link the CDN stylesheet** ahead of app CSS; never vendor a copy of it (Step 0).
> 2. **Dark is opt-in and the host picks it** — read `?theme=`, never ship a switcher (Step 5).
> 3. **The app fills the frame** — no outer gutter, no root width cap; controls cap at 364px (Step 4).
> 4. **Paint `body` yourself** — the dark build's reset still ships `#fff` (Step 5).
> 5. **CSS only, no JS on the CDN** — `.modal`, `.dropdown-menu`, `.collapse`, tooltips and tabs
>    are styling alone; wire the behaviour yourself.
> 6. **Use the bundle's classes** — not in `references/classes.txt` means the bundle doesn't style
>    it. No re-implemented components, no competing `font-family`, no second icon set.
> 7. **The bundle is not self-sufficient** — 28 undefined custom properties, several components
>    without their foundation. Check `references/gaps.md` before you debug one.
> 8. **Restraint is a rule, not taste** — the plainest markup that reads correctly (Step 2).

Canonical sources (lists verified against the live bundle **2026-08-25**, `references/gaps.md`
built against the 2026-08-20 build and re-measured in Chrome 2026-08-25). **If today is more than three months past that date, run
`references/refresh.sh` before trusting any count, class list or token value in this file** — it
takes seconds, needs nothing but `curl`, and prints only what drifted. The bundle ships
independently of this skill, so an old date is the one thing here that cannot be reasoned about:

| What | Where |
|---|---|
| The stylesheet | `https://cdn.sendpulse.com/dist/css/sp-marketplace-app-ui.min.css` |
| CSS / typography / forms / buttons docs | `https://login.sendpulse.com/dist/ui-library/index.html` |
| Component docs | `https://login.sendpulse.com/dist/ui-library/components.html` |
| JS-driven component docs | `https://login.sendpulse.com/dist/ui-library/javascript.html` |
| Icon browser | `https://sp-icons.netlify.app/` |

## Step 0 — Wire it up

**Start from the baseline files in this skill — don't retype them.** Copying them is the
difference between "uses SendPulse classes" and "looks like SendPulse":

Each file is used one of four ways, and the label says which: **COPY** it into the app verbatim,
**READ** the one relevant section, **LOOKUP** a name in it, **SHELL** run it. With no filesystem —
a chat window rather than an agent — the COPY and LOOKUP files are the ones to paste in as
attachments; `adapters/README.md` maps that route per tool.

| Use | File | What it is | When |
|---|---|---|---|
| COPY | `examples/settings-screen.html` | a whole form-shaped screen, composed: panel-as-layout, capped controls, a switcher row, mapping rows, footer | starting any screen — copy the structure, then swap the content |
| COPY | `examples/amazon-connections-screen.html` | the other shape: a plan-gated list of connected things — the `paid` family, separated `.list-group` cards, a row kebab with its JS, a text-first empty state | a screen that lists connections, or anything a pricing plan gates |
| READ | `references/components.md` | the component catalogue of Step 2: every load-bearing class with the markup it needs | building any component — read the one section |
| READ | `references/gaps.md` | the diagnostic catalogue of Step 6: sixteen classes that look like they should work and don't, one section each — symptom → cause → fix | when a class misbehaves — grep it by name, read that section |
| COPY | `references/starter.html` | the correct `<head>`: both theme builds linked, load order, the 20-line theme switch | starting any standalone app |
| LOOKUP | `references/tokens.md` | the light palette as lookup: brand, greys, borders, the four semantic families, the three reds | you need a literal colour and no semantic class covers the case |
| COPY | `references/tokens.css` | the 28 custom properties the bundle reads and never defines, light + dark, plus `color-scheme` | always — link after the bundle |
| COPY | `references/bundle-fixes.css` | the structural gaps of Step 6 as copy-paste CSS: the `.nav` foundation, status-dot specificity, the `.input-group` flex row, `.badge-paid` and `.avatar` alignment | always — take the whole file |
| COPY | `references/kitchen-sink.html` | every load-bearing component rendered correctly in one page, both themes | copy markup from here instead of retyping it from prose |
| SHELL | `references/check-build.sh` | the wiring checker: the CDN link, `tokens.css` and `bundle-fixes.css`, load order, the theme pair, `var()` names — no Node, no browser | any repo, pre-commit |
| SHELL | `references/check-classes.sh` | greps your templates for classes the bundle doesn't define — no Node, no browser | any repo, any framework, pre-commit |
| SHELL | `references/verify.mjs` | the same lookup against the rendered DOM, plus 19 more checks, in Playwright | before you call any screen done |
| SHELL | `references/refresh.sh` | re-derives `classes.txt`, `icons.txt` and the token list from the live CDN and diffs them | when this skill feels stale, or a class you expect is missing |

Two more files, `references/classes.txt` and `references/icons.txt`, are **LOOKUP** — never copied
into an app, just grepped when you need to know whether a name exists.
See *Looking a name up* at the end.

**Load order is the contract:** CDN bundle → `tokens.css` → `bundle-fixes.css` → the app's own CSS
last. Everything in those two files is single-class or lower specificity on purpose, so loading
after the bundle is what lets them win. Beyond them, app CSS should be small enough to read in one
screen, and every rule in it should carry a comment saying which bundle gap or design measurement
it exists for. A growing app stylesheet is the signal that a class was missed, not that the bundle
is short.

In `index.html`, ahead of the app's own stylesheets so app CSS can override it:

```html
<link rel="stylesheet" href="https://cdn.sendpulse.com/dist/css/sp-marketplace-app-ui.min.css">
```

**Any framework, or none.** This is a stylesheet and a class vocabulary, so nothing here is tied to
a framework — the same classes produce the same screen in Angular, React, Vue, Svelte, a server
template, or a hand-written `.html` file with no build step. Only the plumbing differs:

| Setting | The three files go |
|---|---|
| plain HTML, no build | `<link>` them in `<head>` in the order above — `references/starter.html` is literally this |
| any bundler (Vite, webpack, esbuild) | `import "./tokens.css"` etc. from the entry module, or `<link>` them from `index.html` |
| Angular CLI | the `styles` array in `angular.json`, or `@import` from the global stylesheet; component styles are too late and too scoped |
| an app that already gets the design system from its own build | out of scope: it has its own `:root` and asset paths, so none of the wiring below applies — see *Scope* above |

Markup in this skill is written as plain HTML with `class="…"`. Translating is mechanical and
nothing else changes: React wants `className`, a framework's conditional or loop replaces the
`*ngIf`/`v-if`/`{cond && …}` you'd otherwise see, and state classes are toggled however your app
toggles classes. **Never** let the framework change the class names — that is the whole contract.

- The bundle `@import`s **Onest** from Google Fonts and sets it on `html, body` itself.
- Icon fonts (`/my.fonts/sp_icons.*`) resolve against the **stylesheet's** origin, so they work
  from any host — don't self-host them.
- It is a **customised Bootstrap 3.3**: BS3 markup patterns apply except where noted below, and
  the `data-toggle="modal|dropdown|collapse|tab|tooltip|popover"` attributes in the docs assume
  Bootstrap 3 JS is loaded — which the CDN does not ship. Those attributes are inert markers; the
  open/closed state is a class you add (`.open`, `.in`, `.active`) by whatever means your app has.
  `references/kitchen-sink.html` does it in ten lines of plain JS with no framework at all.

## Step 1 — Design tokens

**Take every value from the tables below — never guess one, and never lift one from a screenshot.**
Nearly every value is **baked in**: ~1400 selectors carry literal colours, which is why only the
other build can darken them.

**Ship the 28 custom properties yourself — the bundle references them and defines none.**
`--panel-bg`, `--bg-color`, `--input-bg`, `--divider-color`, `--marine-color-light` and 23 more.
Only `--bg-color` carries an inline fallback, so the rest resolve to nothing: `.side-panel` renders
transparent, focus rings vanish. Inside `login.sendpulse.com` the host shell supplies them; a
standalone integration has no host shell, so it must ship them itself. This is a packaging
boundary, not a bug: in the product those blocks come from `template.min.css`, which an integration
does not link. Copy `references/tokens.css` — it is all 28, light and dark. With no filesystem,
reproduce it from the block in `adapters/chatgpt/instructions.md`; there is no shorter path, because
the names cannot be guessed.

**Copy `references/tokens.css` — never hand-write these.** Guessed values look plausible and are
wrong: `--bg-color` is `#f2f5f5`, not `#fff`; `--base-color` is `#000`, not the `#023346` ink. The
file holds every value that exists — the 28 light, the 12 the dark build overrides — re-verified
against the live CDN 2026-08-21. Nine of the 28 are defined in no stylesheet at all, so the file
carries the best available value for them rather than a lifted one. `references/refresh.sh`
re-derives it; `--vk-brand-color` is the one that cannot be generated, since no build emits it —
it comes from the design system's own `vk-brand-color` source variable (`#5181b8`).

**Never copy a `var()` name out of another integration — check it against `tokens.css` first.**
These 28 are the only custom properties your CSS may reference. An existing integration's CSS uses
about 40, because an app that gets the design system through its own build inherits a larger `:root`
with it; on the CDN path those extras resolve to nothing. Nine of the 28 (`--panel-heading-bg`,
`--size-count`, `--status-color-*`) are defined **nowhere at all**, and shipped screens do read
them: a heading painted with `var(--panel-heading-bg)` and no fallback renders transparent in every
theme. Where a name is absent, use the literal value directly (`24px`, not
`var(--gutter-size-lg)`) — the metrics are below, the colours in `references/tokens.md`.

The metrics, which no class supplies for you:

| Token | Value | Notes |
|---|---|---|
| Font | `'Onest', 'Nunito Sans', -apple-system, …` | weights 400 / 600 loaded; buttons use 700 |
| Base | `16px` / line-height `1.4286` / text `#000` | body background: the app ships `var(--panel-bg)` (`#fff`) — the bundle's own reset says `#fff` in **both** builds, which is the bug `bundle-fixes.css` closes |
| Radius | `8px` controls · `10px` panels/`.btn-lg` · `6px` `.btn-sm`/`.btn-xs` | |
| Control height | `40px` (`.form-control`, `.btn` padding `9px 12px`) | |

Headings: `h1` 40px · `h2` 24px · `h3` 20px · `h4` 20px · `h5` 16px · `h6` 14px.

**Reach for a semantic class before a hex** — `.text-danger`, `.bg-success`, `.color-primary`,
`.color-muted-link`. Hardcode a colour only where no class covers the case, and then take the value
from `references/tokens.md`: the brand blue, the greys, the borders, the four semantic families, and
the three reds that are three different roles and must not be swapped. Not from a screenshot, and
not from another integration's stylesheet.

## Step 2 — Component vocabulary

**The catalogue is `references/components.md`** — buttons, forms and selects, switchers, repeating
rows, panels, alerts, the paid/plan family, labels and badges, modals and side panels, dropdowns,
tables, lists, selector boxes: each with the markup it needs and the traps in picking it. Read the
section for the thing you are building. `references/kitchen-sink.html` renders all of it, so copy
markup from there rather than retyping it, and `examples/` shows the same classes assembled
into two whole screens — order, spacing and what gets left out. `references/classes.txt` is the
full flat list.

One rule is not lookup, because it applies to everything in that catalogue:

**Restraint — the plainest thing that reads correctly.** The bundle is a large vocabulary and it is
tempting to spend it. Don't. Chrome that carries no information is what makes a screen stop looking
like SendPulse.

- **No decorative icons.** A glyph earns its place only when it *is* the control (an icon-only
  button), *is* the state (a `.badge-status` dot), or *is* an identity (`.social-icon`, a brand
  mark). Tabs, nav items, headings, panel titles, labels, table headers, list rows, alerts and any
  button that already has a verb take **plain text**: `<li><a>Forms</a></li>`, not
  `<li><a><i class="sp-icon icon-form-new"></i> Forms</a></li>`.
  Two glyphs pass that test so reliably they are the house pattern rather than a judgement call,
  both in *Repeating rows* in `components.md`: `icon-trash` in an icon-only `.btn-icon` for removing one row,
  and `icon-plus-add` on the "add another" link. Everywhere else the rule stands.
- **One primary button per view.** Everything secondary is `.btn-default` or `.btn-link`.
- **One signal per state.** A row does not need a status dot *and* a coloured label *and* an icon
  all saying "connected". Pick one.
- **Don't decorate structure.** No panel inside a panel, no `.well` wrapped round two fields to
  "group" them, no `.alert` standing in for a heading.
- **Colour is semantic, never variety.** `.text-danger` and `.badge-status-success` mean something;
  a tab strip is not a palette.
- **Empty and loading states are text first** — a sentence and a `.btn-link` before an illustration.
- Every element left out is one that cannot go stale, mistranslate, or fight the dark build.

## Step 3 — Icons

```html
<i class="sp-icon icon-envelope" aria-hidden="true"></i>
```
- Always both classes: `sp-icon` (the `sp_icons` font) **and** `icon-NAME`. No inner text.
- 536 names in `references/icons.txt`, visual browser at https://sp-icons.netlify.app/.
- **No font-size of its own** — the glyph inherits from its context (16px in body text). 18px is a
  context rule, not a default: `.btn-more-action .sp-icon` and
  `.dropdown-item-options > .btn > .sp-icon` are the rules that set it. Colour is inherited too;
  tint with `.color-primary` / `.color-default` / `.color-danger` rather than inline styles.
- **`.sp-icon` has no margin of its own.** Spacing comes only from context rules —
  `.btn .sp-icon` 3px, `.dropdown-menu a .sp-icon` 5px, `.dropdown-item-long .sp-icon` 10px.
  Anywhere else (a tab, a heading, a list row) the label sits flush against the glyph: add the
  bundle's `.margin-right-5`. That utility and `-10` / `-30` are the only three defined.
- Decorative icons get `aria-hidden="true"`; an icon-only button needs an `aria-label`. Better
  still, don't add a decorative icon at all — see *Restraint* at the end of Step 2.
- Brand marks come from a separate `social-icon` font, addressed by number: `.social-icon.social-icon-3`
  (ids 1, 3–8, 1000–1004, 1006, 1007 — there is no 1005). There is no name-based alias — check `references/classes.txt`.
- Never mix in Font Awesome, Material Icons, or inline SVG for something `sp_icons` already has.
- **The name does not tell you the shape.** 536 glyphs share a handful of stems, and the plainest
  name is often the decorated variant: `icon-plus` is a plus inside a rounded box, `icon-plus2` and
  `icon-add` are pluses inside a circle, and the **bare** plus is `icon-plus-add`. Look at the
  candidates in the icon browser (or render them side by side) before picking one — the cost of
  guessing is a boxed glyph on an "Add link" row that nobody notices in review.

## Step 4 — Layout and spacing

**The app fills the frame it is handed and never sizes itself.** An integration is not a web page —
it is a web resource SendPulse opens **in an iframe** that it has already positioned, already inset,
and already sized and scrolling. **The size depends on where the integration is shown**, so it is
never a number the app can assume:

| Where | Frame |
|---|---|
| integration settings in the marketplace | **796px** wide |
| a widget window | a different size, and not one to hardcode |

So an app that caps or centres itself is wrong in the settings screen, and wrong by a *different*
amount in a widget. The host owns the page chrome; the app owns whatever rectangle it is handed, and
fills it. Anything the app adds on the outside is added *on top of* the host's own inset, so it
reads as double padding and the panel stops meeting the frame edge. The outermost element of an
integration therefore carries **no margin, no padding and no `max-width`**:

- **No outer gutter.** The 24px rhythm belongs *inside* the panel — `.panel-body` already has it.
- **No width cap on the root.** Not even 796px: in the settings screen the frame is already that
  wide, so the cap is a no-op — and in a widget of another size it leaves the frame empty on both
  sides. A cap on the root cannot be right in both places. Caps belong on the wrapper around
  one form control, one level in, at 364px — *Controls do not stretch*, below.
- **No centring.** `margin: 0 auto` is the same mistake stated differently.
- **Full height when the screen has a footer.** A sticky action footer needs the app to be as tall
  as the frame: `html, body, #root { height: 100% }` and a flex column. Not `100vh` — inside an
  iframe that is the iframe's own height only when the host happened to size it that way.
- **The host is the only scroller you can count on.** Don't put `overflow` on the app root to make
  your own scroll region; the marketplace already scrolls the iframe.

The panel is the layout: `.panel` flush to the frame edge, its own `.panel-body` padding doing the
insetting. `examples/settings-screen.html` is that whole screen, with the capped controls and the
full-width mapping rows side by side.

**The Bootstrap column grid is not in this bundle.** There is no `.container`, no `.col-md-6`,
no `.col-lg-*` — only `.row`, `.row-flex`, `.col-sm-6` and `.col-flex` / `.col-flex-sm|md|lg`.
Lay out with the flex utilities instead:

`.d-flex` `.d-inline-flex` `.d-block` `.d-inline-block` `.d-none` ·
`.flex-row|column(-reverse)` `.flex-wrap` `.flex-nowrap` `.flex-fill` `.flex-grow-0|1` `.flex-shrink-0|1` ·
`.justify-content-start|end|center|between|around` · `.align-items-start|end|center|baseline|stretch` ·
`.align-self-*` · `.align-content-*`

**Controls do not stretch — cap each one, not the screen.** The panel takes the full frame, but a
`.form-control` inside it never does: a text input stretched to the full width of a settings frame
reads as a mistake, and every shipped integration caps its fields. The cap goes on the **wrapper around one control** — the div holding
its label, the control and its help text — and there are three widths in use:

| Width | For |
|---|---|
| **364px** | the default: every select, text input, number field. Some screens use 360px — either reads as the same column, so pick one and keep it |
| **420px** | a field whose content genuinely needs the room. The bundle's `.width-limit-xnarrow` is this width |
| **540px** | rare, one long field |

```html
<!-- the cap rides on the .form-group: one wrapper per control, not one column round the form -->
<div class="form-group app-form-mw spacing-bottom-lg">
  <label class="control-label" for="pipeline">CRM pipeline</label>
  <select class="form-control" id="pipeline">…</select>
  <span class="help-block">Deals are created in this pipeline.</span>
</div>
```

```css
.app-form-mw { max-width: 364px; }   /* the design's control width — not a guess */
```

`.width-limit-xnarrow` (420px) is the closest thing the bundle ships; 364px has no class, so it is
app CSS on one named wrapper — never a `width` on each `.form-control`, and never a cap on the
panel or the root (above).

Per control is what the shipped integrations do, and it is what survives a form that interleaves
narrow fields with full-width things — a divider, a mapping table, an item row. Where several
capped controls genuinely do sit one after another with nothing wide between them, one wrapper
round the group is the same result with less markup (`references/kitchen-sink.html` does that).

**What does take the full width:** mapping rows, connected-item rows, tables and anything else
whose columns need the room. Those stretch, and the 24px of `.panel-body` is their only inset. The
other `.width-limit*` classes (`.width-limit`, `-narrow` 790px, `-wide`) cap something as wide as
the frame itself, so on these screens they do nothing useful.

Spacing: prefer the semantic scale — `.spacing-top`/`.spacing-bottom` with `-xs|-sm|-md|-lg|-xl|-none`.
The numeric `.margin-*` / `.padding-*` classes exist only for a scattered handful of values
(check `references/classes.txt` before using one — most numbers are not defined).

Responsive visibility: `.hidden-xs|sm|md|lg`, `.visible-xs|sm|md|lg(-block|-inline|-inline-block)`,
`.hidden-print` / `.visible-print-*`. Breakpoints: 480 · 768 · 992 · 1200px.

## Step 5 — Theming

Light and dark are **server-rendered builds of the same URL**, not a media query (verified
against the CDN, 2026-08-20).

- Plain URL and `?force=light` are byte-identical; `?force=dark` is a separate build.
- Dark recolours the same selectors: `.panel` `#fff`→`#030607`, `.well` `#e6ecec`→`#070c0e`,
  borders `#cdd4d4`→`#1d363f`, text `#000`→`#d6e3e3`. Never hand-write a dark palette, and never
  assume a Step 1 hex survives into dark.
- **The theme is an input, not a control.** The SendPulse host already has the user's theme
  setting and hands it to the integration as `?theme=dark` on the app's own URL. Read it once at
  boot, apply it, and stop — **an integration never ships a theme switcher**. A toggle inside the
  app is a second source of truth for a setting the app does not own: it disagrees with the shell
  around it, survives no reload, and appears in no design. If you want to *see* both themes while
  developing, open `?theme=dark` — that is the same code path the host uses, so it also proves the
  wiring works.
- **The param does not survive navigation.** `?theme=` is on the URL the *host* opened. An in-app
  redirect, an OAuth return, a "open in new tab" link, any URL the app builds itself — all arrive
  without it, and the app silently reverts to light with no error anywhere. Either carry `theme`
  through every hop that constructs a URL, or read it once at boot and keep it for the session.
  The same is true of the `?lang=` and `?access=` params that arrive alongside it: shipped
  integrations re-attach all three to the post-login redirect for exactly this reason.
- Applying it is two lines: ship both `<link>`s, disable one with `media="not all"`, and mirror the
  choice as `ma-light` / `ma-dark` on `<html>` — written out in `references/starter.html`, driven by
  the URL param. A single-theme app links the plain URL and stops.
- **Both builds get fetched that way** (the disabled one at low priority, ~330KB each), which is
  the price of having no flash and no JS-inserted stylesheet. If a server renders the shell, emit
  only the `<link>` the `?theme=` param calls for and set the class in the same response — same
  result, half the CSS, no script at all.
- `.ma-dark` ships in **both** builds and only carries shadow/`filter` fixes — it cannot turn the
  light build dark.
- The dark build's reset still sets `body{background-color:#fff}` — set the page background yourself.
- **Declare `color-scheme` yourself.** Neither build contains the property (0 occurrences in both),
  so native widgets — the `<select>` popup, scrollbars, the date picker, spin buttons, autofill —
  stay light inside the dark build. The dark build *tries*, with
  `select.form-control option{background-color:#030607}`, but that rule lives inside
  `@media not all and (min-resolution:.001dpcm)`, the Safari-only hack, so Chrome and Firefox never
  see it. Two declarations cover every browser:

```css
:root          { color-scheme: light; }
:root.ma-dark  { color-scheme: dark;  }
```

## Step 6 — Gaps the bundle leaves you

Sixteen classes exist, look like they should work, and don't — `.nav-tabs` renders as a bulleted
list, `.side-panel` is transparent, `.badge-status` overflows any text put inside it, a `.modal` is
invisible. **The catalogue is `references/gaps.md`**: symptom → cause → fix, one section per class,
indexed at the top of the file. Grep it for the class you are fighting and read that section before
concluding you've used the class wrong. **No filesystem?** The whole sixteen-row index — class,
symptom, what closes it — is reproduced under *The gaps* in `adapters/chatgpt/pocket-guide.md`;
that table is enough to know which gap you hit, and only the argued-out cases need the full file.

Most of it is boilerplate you never write: `references/tokens.css` and `references/bundle-fixes.css`
between them close seven of the sixteen, which is why Step 0 says copy both. The rest are decisions,
and `references/gaps.md` is where they are argued out.

## Step 7 — Check the result mechanically

Three checkers ship in `references/`. They answer different questions, and none of them replaces
looking at the screen in both themes. **No shell?** Then walk the checklist in
`adapters/chatgpt/pocket-guide.md` instead — it is these same assertions in manual form, and the
four that matter most are: every class name found in `classes.txt`, the CDN link first with
`tokens.css` and `bundle-fixes.css` after it, every `var()` name among the 28, and the app root
carrying no padding, cap or centring.

**The wiring, before anything else.** `check-build.sh` reads the repo — no Node, no browser — and
catches what fails silently here: a self-hosted bundle (every glyph breaks, since `url(/img/…)`
resolves against the stylesheet's origin), a missing or misordered `tokens.css` / `bundle-fixes.css`,
app CSS ahead of the fixes, both builds live at once, `ma-dark` off the root, a `var()` name no
stylesheet defines, `prefers-color-scheme` in app CSS. FAIL means broken; WARN means look.

```bash
references/check-build.sh path/to/integration     # or no argument, for the current repo
```

**The class names.** The mistake that most reliably stops a screen looking like SendPulse is a class
the bundle never defined — a typo, a half-remembered name, an invented one. Two scripts catch it;
take whichever your repo can run. Grep only, works anywhere:

**Copy `references/` into the repo** (`tools/sp-ui/`, say) and run it from there, or call it by its
full path in this skill — either way the scripts find `classes.txt` beside themselves:

```bash
tools/sp-ui/check-classes.sh --app-prefix app- $(find src -name '*.html')
```

It reads `class="…"`, `className="…"` and `className={\`…\`}` out of the source, so plain HTML,
JSX, Angular and Vue templates all work, and reports every name that is in neither `classes.txt`
nor `icons.txt`. Names your code assembles at runtime (`"badge-status-" + status`) are invisible to
it, and nothing about rendering is checked — for that:

**With Node — the rendered page.** `references/verify.mjs` opens it in real Chrome, **in both
themes**, and exits 1 on any finding:

```bash
npm i -D playwright && npx playwright install chrome    # once, in the app repo
node tools/sp-ui/verify.mjs http://localhost:5173 --app-prefix app-
```

Its first check is the same lookup, but against the **live DOM**, so runtime-composed names are
covered too. The other nineteen turn this skill's own rules into assertions: the undefined custom
properties, `color-scheme`, the body the dark reset leaves white, a `glyphicon-*`, a non-Onest font,
the frame rules, icon a11y, a theme switcher — and every Step 6 gap a rendered page can be measured
for (the stacked `.input-group`, unfloated `.nav-tabs`, a status dot grey inside a
`.list-group-item`, the `.avatar` off its baseline, a `.modal` with no backdrop, the toggle knob over
its label, and the four styled-but-inert classes). `--app-prefix` declares your own classes (`app-`, whatever the repo uses); the classes
`bundle-fixes.css` introduces are read out of that file, so the two never drift. Both scripts work
off the shipped list rather than asking the bundle, and have to: the CDN sends
`access-control-allow-origin: https://login.sendpulse.com`, so neither a shell nor a local page can
read the stylesheet's own rules.

It loads the dark pass as `?theme=dark` — the host's own path — so a run also proves the app reads
the param instead of exposing a toggle.

**Changing a screen that already exists.** Everything above assumes a new screen; most work isn't.
On an existing integration the checkers will report the app's own vocabulary as unknown — measured
against four shipped integrations, they carry **15–29 distinct class prefixes each**, not one. That
is not a backlog to fix:

- **List the prefixes, don't fix the screen.** `--app-prefix` is repeatable and takes a
  comma-separated list. Declare what the repo already uses, and what remains is the short list worth
  reading. One repo went from 166 findings to a handful this way.
- **Never declare a prefix the bundle owns.** `--app-prefix color-` silences a real bug: the bundle
  has `.color-muted-link`, not `.color-muted`, and `.gap-5`, not `.gap-xl`. A near-miss name is
  exactly what the check exists to catch, so keep those families reportable.
- **Fix what you touch, not what you find.** Pre-existing findings in a screen you are editing are
  not yours to clear, and a "while I'm here" rewrite is how a small change becomes unreviewable.
  Bring your component up to the vocabulary and leave the rest, noting anything alarming.
- **On the other delivery route, treat the output as a review list.** `classes.txt` is the CDN
  bundle. An app that gets the design system through its own build has a larger vocabulary, so a
  name missing here may be perfectly real there (see *Scope*).

**It is a floor, not a verdict.** Clean output means nothing is provably wrong, not that the screen
looks right — spacing, hierarchy and restraint still need your eyes on it in both themes.
`references/kitchen-sink.html` passes clean — `--app-prefix ref-`, since its own page furniture is
`ref-*` — so it is also the control: if anything else fires there, suspect the checker.

## Checklist before delivering

`references/check-build.sh`, `references/check-classes.sh` and `references/verify.mjs` assert most of
this skill mechanically — run them first (Step 7), then check by eye only what a script cannot see:

- [ ] **Run the checkers** — or, with no shell, walk the manual list in
      `adapters/chatgpt/pocket-guide.md`. `check-build.sh` clean on the repo, `check-classes.sh`
      clean over the templates and, where Node is available, `verify.mjs` clean in **both** themes.
      Between them
      they cover the CDN link, both required files and their load order, the theme pair and
      `ma-dark`, `var()` names, invented classes in the source *and* the DOM, and the Step 6 gaps.
      Everything they cover is off this list.
- [ ] **App CSS is short**, and every rule in it names the bundle gap or design measurement it
      exists for — no colours, no re-styled components. A growing stylesheet means a class was missed.
- [ ] **Nothing the bundle already styles was re-implemented**, and no hardcoded colour stands where
      a semantic class exists.
- [ ] **Restraint holds** (Step 2): no decorative icons, one primary button per view, one signal per
      state, no panel inside a panel. A checker counts glyphs; it cannot tell you one is pointless.
- [ ] **The house patterns are used where they apply** — repeating rows with `.btn-icon` +
      `icon-trash` and `icon-plus-add` (`components.md`), plan gating through the
      `.alert-paid` / `.badge-paid` family with the promo SVG resolvable.
- [ ] **The right icon, not just a real one** — `icon-plus` is boxed, `icon-plus2`/`icon-add`
      circled, the bare plus is `icon-plus-add` (Step 3). Every name here passes the class check.
- [ ] **Interactive components have behaviour wired up** — the CSS alone does nothing (Step 6).
- [ ] **Eyeballed in both themes.** Spacing, hierarchy and restraint are the part the scripts
      cannot judge: clean output means nothing is provably wrong, not that the design is right.

---

## Looking a name up

Two flat lists ship beside this file. They answer one question — *does the bundle style this, or am
I inventing it?* — and a miss means don't use the name, not "add a rule for it". One name per line,
so `grep -x` is an exact check and a bare `grep` browses a family.

```bash
grep -qx 'panel-title'  references/classes.txt   # 1411 classes the bundle defines (2026-08-21)
grep    -i 'plus'       references/icons.txt     # 536 sp_icons names, `icon-` prefix omitted
references/refresh.sh                            # both lists are generated — re-derive, don't trust the date
```

The bundle also still carries **97 Bootstrap `glyphicon-*` classes**, a second icon font inherited
from BS3 and not part of the design system. They are deliberately absent from `classes.txt` so they
can't be picked by accident — a glyphicon missing from the list means don't use it, not that the
list is stale. Use `sp-icon icon-*` (non-negotiable #6). `refresh.sh`'s own header covers the rest:
what `--write` rewrites, what it only reports, and what to do with a drift line.


## Version and updates

With web access you MAY, once per conversation, compare the `version` above against
`https://raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-marketplace-ui-cdn/VERSION`
and mention a newer one — then carry on with this version regardless. Never block on the check.

The design system moves independently of this skill, so **when the live bundle and this file
disagree, the bundle wins** — `references/refresh.sh` is how you find out, and it takes seconds.
Change history: [CHANGELOG.md](CHANGELOG.md).
