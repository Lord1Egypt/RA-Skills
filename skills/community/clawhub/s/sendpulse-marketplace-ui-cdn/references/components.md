# Component vocabulary

The load-bearing classes of `sp-marketplace-app-ui.min.css`, with the markup each one needs. This
is the catalogue SKILL.md Step 2 points at: read the section for the component you are building,
not the whole file. The full flat list of every class the bundle defines is `classes.txt`; this
file is the subset that carries a screen, plus the ones whose markup is not guessable.

Two rules from Step 2 stay in SKILL.md rather than here, because they apply to every component on
this page: *Restraint* (what to leave out) and the non-negotiables. Nothing below repeats them.

`kitchen-sink.html` renders everything on this page, correctly, in both themes — copy markup from
there instead of retyping it from prose.

Verified against the live bundle 2026-08-21.

---

Full list in `references/classes.txt`. The load-bearing ones:

## Buttons

`.btn` + one variant, optionally one size.
```html
<button class="btn btn-primary">Save</button>
<button class="btn btn-default btn-sm">Cancel</button>
<button class="btn btn-primary" disabled>Saving…</button>
<a class="btn btn-link" href="#">Learn more</a>
<button class="btn btn-icon"><i class="sp-icon icon-pencil"></i></button>
```
- Variants: `btn-primary` `btn-default` `btn-success` `btn-danger` `btn-warning` `btn-info`
  `btn-link` `btn-outlined` `btn-outlined-white` `btn-dashed` `btn-icon` `btn-block`.
- Sizes: `btn-lg` (20px) · default (16px) · `btn-sm` (14px) · `btn-xs`.
- One primary action per view; everything secondary is `btn-default` or `btn-link`.
- Social sign-in: `.btn-social` + `.btn-fb` / `.btn-google` / `.btn-tg` / `.btn-wa` / `.btn-vb` / `.btn-in`.
- Loading state: `.btn-loading`. Groups: `.btn-group`, `.btn-toolbar`.

## Forms

Always `.form-group` + `<label>` + `.form-control`; every control gets a real label.
```html
<div class="form-group has-error">
  <label class="control-label" for="email">Email</label>
  <input type="email" id="email" class="form-control" placeholder="name@example.com">
  <span class="help-block">Enter a valid address.</span>
</div>
```
- Validation: `.has-error` / `.has-warning` / `.has-success` on the `.form-group`, message in
  `.help-block`. `.has-feedback` + `.form-control-feedback` for the inline icon.
- Sizes: `.input-sm` / `.input-lg`, or `.form-group-sm` / `.form-group-lg`.
- Layouts: `.form-horizontal`, `.form-inline`, `.form-row`. Read-only display: `.form-control-static`.
- Composites: `.input-group` with `.input-group-addon` / `.input-group-btn`.
- **`<select>`**: a plain `<select class="form-control">` is the sanctioned control — that is what
  the official UI-library page itself uses, and it is fine. Its option list is painted by the OS,
  which the design system accepts rather than fights: it ships
  `select option{font-family:-apple-system,…}`, deliberately handing the list the system font. The
  one thing to add is `color-scheme` (SKILL.md Step 5), so the popup follows the theme instead of opening
  light inside a dark page. Do **not** rebuild a select out of divs to get a themed popup.
- **For a rich row — an avatar, a coloured initial disc, a status label — you do not need a
  plugin.** The bundle deliberately styles a dropdown trigger to look exactly like an input:
  `.form-control.dropdown-toggle` gets `position:relative`, `.caret` is placed inside it
  (`right:10px;top:18px`), and the open state gets the same focus ring as a focused control. This
  is what the Application marketplace designs use for every avatar/label select.

```html
<div class="dropdown">
  <button class="form-control dropdown-toggle text-left" data-toggle="dropdown">
    <span class="avatar avatar-24 margin-right-5"></span> Valerii Sereda
    <span class="caret"></span>
  </button>
  <ul class="dropdown-menu dropdown-menu-wide">…</ul>
</div>
```

- Only a select needing **search, groups or multi-select** goes further, to the bootstrap-select
  plugin — the bundle carries its skin but none of its structure, which is a trap; see `gaps.md`
  before choosing it. Whatever you build, the real `<select>` stays in the wrapper as the value
  carrier: never a div that replaces one.
- Checkboxes/radios use the `.checkbox` / `.radio` / `.checkbox-inline` wrappers, not bare inputs.
- **A switcher is an input followed by an empty label, tied by `for`/`id`** — the track and knob are
  drawn entirely by `.switcher-toggle + label` and its `:after`, so there is no inner span to add
  and the order is not negotiable. Use it for a whole feature on/off, with `.switcher-flex-holder`
  putting it at the right edge of a row whose left side is a bold label plus one description line;
  a sub-option inside a form stays a `.checkbox`.

```html
<div class="switcher">
  <input class="switcher-toggle" id="two-way" type="checkbox">
  <label for="two-way" aria-label="Two-way sync"></label>
</div>
```

## Repeating rows

A variable mapping, a list of conditions, anything the user adds more of.
Two controls recur, and both are the one place a glyph is right rather than decoration:

```html
<div class="d-flex align-items-center gap-5">
  <select class="form-control">…</select>
  <span class="text-muted">to</span>
  <select class="form-control">…</select>
  <button class="btn btn-icon" aria-label="Remove mapping 1">
    <i class="sp-icon icon-trash" aria-hidden="true"></i>
  </button>
</div>
<button class="btn btn-link">
  <i class="sp-icon icon-plus-add" aria-hidden="true"></i>
  <span class="dashed">Add variable</span>
</button>
```

- **The row's remove control is icon-only** — `.btn-icon` + `icon-trash`, with an `aria-label`
  naming the row. Not the word "Remove": it repeats down the column, reads as heavy as the fields
  it sits beside, and translates to a different width in every locale. This is the *is the control*
  case of *Restraint*, not an exception to it.
- **The add control is a bare plus plus a dashed-underlined label.** `icon-plus-add` is the plain
  plus (`icon-plus` is boxed, `icon-plus2`/`icon-add` circled — SKILL.md Step 3). The underline comes from
  the bundle's `.dashed` (`border-bottom:1px dashed;text-decoration:none!important`), and it goes
  on a `<span>` around the text alone — put it on the button and the rule runs under the glyph and
  the padding too. `.dotted` is *not* the class for this: bare, it only sets `border-style` on a
  `.btn`, and it draws an underline only on `a.dotted[data-toggle=collapse|dropdown]`.
- Inside a `.btn` the bundle already spaces the glyph (`.btn .sp-icon{margin-right:3px}`), so no
  `.margin-right-5` here.

## Panels

The default content container (white, 10px radius):
```html
<div class="panel panel-default">
  <div class="panel-heading"><h3 class="panel-title">Settings</h3></div>
  <div class="panel-body">…</div>
  <div class="panel-footer">…</div>
</div>
```
Use `.well` for a recessed grey block, `.panel` for a raised card. Don't nest a panel in a panel.

## Alerts

Inline, page-level messages — `.alert` + `.alert-success|info|warning|danger`, plus
`.alert-dismissible` with a `.close` button when dismissible. `.alert-sm` for compact.
Transient feedback uses the toast classes (`.toast-container` + `.toast-success|info|warning|error`),
never an alert injected at the top of the page.

## Plan gating — the paid alert

SendPulse features sit behind pricing plans, so an integration
that touches a paid feature (CRM, telephony, a Pro-only field) must say so rather than silently
disabling a control. The bundle ships a whole purple `paid` family for exactly this — use it, never
a hand-written "please upgrade" box.

```html
<!-- feature unavailable on the current plan -->
<div class="alert alert-paid has-paid-badge">
  <span class="badge badge-paid">&nbsp;</span>
  Your CRM pricing plan has expired.
  <a href="https://login.sendpulse.com/crm/plans" target="_blank">upgrade your pricing plan</a>
</div>

<!-- the badge alone, marking one gated control -->
<span class="badge badge-paid badge-paid-sm">&nbsp;</span>
```

- `.alert.alert-paid` — purple wash (`rgba(119,56,237,.1)`), 8px radius, no border, no shadow; its
  `<a>` is `#7738ed`. `.alert-sm` for the compact variant.
- `.has-paid-badge` reserves the left inset (48px, or 42px with `.alert-sm`) and absolutely
  positions the `.badge-paid` in it. So the badge must be the alert's **own child**, and it must
  actually render — ship `&nbsp;`, because an empty inline span collapses.
- `.badge-paid` is an 18px gradient disc with the promo glyph in `:after`; resize with
  `.badge-paid-sm` (15px) / `.badge-paid-lg` (30px). Plan modifiers repaint it and swap the glyph:
  `.plan-standard` `.plan-pro` `.plan-enterprise` `.plan-crm_basic` `.plan-crm_lite`. The same
  modifiers on `.alert-paid` tint the alert to match that plan.
- Rest of the family: `.btn-paid` / `.link-paid` (purple call to action), `.label-paid` (gradient
  pill), `.badge-pro`, `.badge-paid-bf` (dark Black-Friday pill). Callout arrows:
  `.has-top-arrow` / `.has-left-arrow` / `.has-bottom-arrow`, nudged by `.alert-arrow-top-right`.
- **Where it goes.** One alert at the top of the gated page's `.panel-body`, rendered only when the
  account lacks the plan, with the gated controls `disabled` and a small `.badge-paid` beside each.
  The copy holds the upgrade link as inline HTML, so it must be rendered as markup rather than
  escaped text — otherwise every locale loses the link. That is the shipped pattern across
  integrations; copy the wording from one rather than reinventing it.

**The glyph's URL needs nothing from you.** `.badge-paid:after` loads
`url(/img/my/sp-i-promo-md.svg)`, root-relative — which resolves against the *stylesheet's* origin,
so linking the CDN it lands on `cdn.sendpulse.com` and works (verified 200, 2026-08-21). Change
nothing. It only breaks if the CSS is compiled or vendored into your own origin, which is
non-negotiable #1 restated: this badge is the cheapest way to notice you did.

## Labels & badges

`.label` + `.label-primary|success|warning|danger|info|default`, plus SendPulse
extras (`.label-sp-default`, `.label-outlined`, `.label-pro`, `.label-promo`, `.label-tag`).
A count is a plain **`.badge`** — a 14px pill on `#465152`, `vertical-align:middle`, and the bundle
already nudges it where it belongs: `.nav-tabs > li > a .badge{margin-top:-1px}`,
`.nav-pills > li > a > .badge{margin-left:3px}`, `.well .badge, td .badge{margin-top:-1px}`. So a
tab counter needs no extra class at all.

**`.badge-counter` is not "the small round one" — it is an overlay**, and picking it for an inline
count is the usual mistake. It is `position:absolute;right:-8px;top:8px`, red `#f15845`, sized for
a notification dot sitting *on* an icon-shaped control (that is what `.noty-button .badge` does).
Inside a tab it is torn out of the text flow and hangs off the label; in an unpositioned row it
flies to the nearest positioned ancestor, usually a page corner. Use it only on a control that is
itself `position:relative`, and only when the number should overlap the control rather than follow
its label.

`.badge-status-success|warning|danger|primary` is **a 10×10px dot, not a text pill** — it is
`width:10px;height:10px;padding:0`, so text put inside it overflows and clips. Pair it with a
sibling label: `<span class="badge badge-status badge-status-success"></span> Connected`. Add
`.status-donut` for the hollow-ring version of the same dot (a 2px inset ring, useful for an
inactive state) — its centre is `var(--panel-bg)`, so it depends on a property the bundle never
defines (SKILL.md Step 1) and is otherwise transparent.

## Overlays

`.modal > .modal-dialog > .modal-content` with `.modal-header` / `.modal-body` /
`.modal-footer`; sizes `.modal-sm` `.modal-md` `.modal-lg`. A drawer sliding from the edge is
`.modal-side`, or the standalone `.side-panel` family (`.side-panel-header`, `.side-panel-content`,
`.side-panel-footer`, `.side-panel-collapsed`). Footer buttons: primary action rightmost.

## Menus

`.dropdown > .dropdown-toggle + .dropdown-menu > li > a`. Variants: `.dropdown-menu-right`,
`.dropdown-menu-wide`, `.dropdown-menu-small`, `.dropdown-menu-scroll`, `.dropdown-menu-has-arrow`,
`.dropdown-header`.

Two of those are load-bearing, not cosmetic, and picking them by feel goes wrong in one direction
each:

- **`.dropdown-menu-wide` is `width:100%`** — of the `.dropdown` wrapper, which is a block. Use it
  only when the trigger *is* a full-width control (the input-shaped `.form-control.dropdown-toggle`
  above). On a kebab, an icon button or a text link it stretches the menu across the whole panel.
  A menu with no width class sizes to its rows off `min-width:160px`.
- **`.dropdown-menu-right`** on any trigger near a right edge — a row's kebab, a panel-corner info
  button. The default `left:0` opens the menu rightwards from the trigger, straight off the panel.

A menu row is styled by `.dropdown-menu > li > a` **only**: a `<button>` in there inherits nothing,
so an action row is an `<a role="button" tabindex="0">` with a keyboard handler, not a button.

## Tables

`.table` plus `.table-striped` `.table-bordered` `.table-hover` `.table-condensed`
`.table-vcenter` `.table-without-border`; wrap in `.table-responsive` for narrow viewports.
Choosing a table over the `.list-group` cards is a content question, not a styling one — a table for
uniform rows with no per-row status, cards once a row has state and actions.
Skip `.table-striped` and the contextual row tints unless the colour means something.

## Lists

`.list-group` / `.list-group-item` (+ `-heading`, `-text`, contextual `-success` etc.),
`.list-unstyled`, `.list-inline`, `.list-divided`. `.list-divided` only draws the rules between
`> li`; it never resets `list-style`, so write `class="list-unstyled list-divided"` or you get
bullets.

`.list-group-item` is built for a **collapsed** list: SendPulse overrides Bootstrap's box to
`border-color:transparent` with only a top rule (`rgba(205,212,212,.6)`) and `margin-bottom:-1px`.
Separated card-style rows — the Application marketplace item lists — therefore need app CSS to put
that rule colour back on all four edges plus the gap — one rule, on one named wrapper class:

```css
.app-item-row {                       /* separated cards, not the collapsed default */
  border: 1px solid var(--divider-color);
  border-radius: 10px;                /* no radius token on this route — SKILL.md Step 1 */
  margin-bottom: 8px;
}
.app-item-row--connected { border-left: 3px solid var(--success-color); }   /* state on the edge */
```

Both `var()`s are in `tokens.css`; the radius is not — the CDN bundle defines no geometry tokens,
so it is the literal from Step 1.

The left border is the row's whole status signal — one signal per state, so no dot and no label
beside it.

## Selector boxes

The SendPulse pattern for "pick one of these options" cards:
`.selector-boxes > .selector-box` with `.selector-box-icon` (+ colour modifier `-blue|-marine|
-purple|-red|-violet|-yellow`), `.selector-box-title`, `.selector-box-descr`, `.selector-box-disabled`.
Prefer this over hand-rolled radio cards.
