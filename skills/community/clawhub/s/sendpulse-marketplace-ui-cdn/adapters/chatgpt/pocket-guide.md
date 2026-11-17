# SendPulse Marketplace UI — pocket guide

Upload this file as *Knowledge* beside the instruction block. It carries what the 8000-character
instruction field could not hold, and the instructions point at it twice: **read the first three
sections before writing markup**, and **walk the checklist before delivering a screen**.

Everything here was verified against the live CDN build of **2026-08-25**. When the live bundle and
this file disagree, the bundle wins.

---

## Icons

```html
<i class="sp-icon icon-envelope" aria-hidden="true"></i>
```

- **Always both classes** — `sp-icon` (the `sp_icons` font) *and* `icon-NAME`. No inner text.
- **536 names live in `icons.txt`**, with the `icon-` prefix omitted there. Visual browser:
  https://sp-icons.netlify.app/. A name that is not in that file does not exist — don't invent one.
- **No font-size of its own.** The glyph inherits from its context (16px in body text). Colour is
  inherited too: tint with `.color-primary` / `.color-default` / `.color-danger`, not inline styles.
- **No margin of its own.** Spacing comes only from a few context rules (`.btn .sp-icon` 3px,
  `.dropdown-menu a .sp-icon` 5px, `.dropdown-item-long .sp-icon` 10px). Anywhere else the label
  sits flush against the glyph — add `.margin-right-5`. That utility and `-10` / `-30` are the only
  three defined.
- **The name does not tell you the shape.** 536 glyphs share a handful of stems, and the plainest
  name is often the decorated variant: `icon-plus` is a plus inside a rounded box, `icon-plus2` and
  `icon-add` are pluses inside a circle, and the **bare** plus is `icon-plus-add`. Look at the
  candidates before picking one.
- **Accessibility.** Decorative icons get `aria-hidden="true"`; an icon-only button needs an
  `aria-label`. Better still, don't add a decorative icon at all — see *Restraint* in the
  instructions.
- **Brand marks** come from a separate `social-icon` font, addressed by number:
  `.social-icon.social-icon-3` (ids 1, 3–8, 1000–1004, 1006, 1007 — there is no 1005). No
  name-based alias exists; check `classes.txt`.
- **Never mix in** Font Awesome, Material Icons or inline SVG for something `sp_icons` already has.
  The bundle still carries 97 Bootstrap `glyphicon-*` classes inherited from BS3; they are not part
  of the design system and are deliberately absent from `classes.txt`. A glyphicon missing from the
  list means don't use it, not that the list is stale.

## Palette

**Reach for a semantic class before any hex** — `.text-danger`, `.bg-success`, `.color-primary`,
`.badge-status-success`, `.color-muted-link`. A literal colour belongs in app CSS only where no
class covers the case, and then it comes from this table — never from a screenshot, an eyedropper,
or another integration's stylesheet.

These are the **light** values. Dark is a separate server-rendered build that recolours the same
selectors, so nothing here survives into it: never hand-write a dark palette.

| Role | Light | Notes |
|---|---|---|
| Primary (brand) | `#009fc1` | links, `.btn-primary`, `.label-primary`, `.text-primary` |
| Link hover | `#006075` | underlined on hover/focus |
| Ink / heading | `#023346` | `.color-muted-link`, `.btn-default` text |
| Muted grey | `#91a4a5` · `#465152` · `#777` | icons · badges · small text |
| Borders / rules | `#cdd4d4` | inputs, `hr`, `legend` |
| Surface grey | `#e1e8e8` (`.btn-default`) · `#e6ecec` (`.well`) · `#f8f9f9` | |
| Success | `#00b175`, text `#006532`, bg `#f2fff5` | |
| Danger | `.btn-danger` `#d94b4d` · `.text-danger` `#b2263f` · status dot `#f86850` | three reds by role — don't swap them |
| Warning | `#f0ad4e`, text `#ac6417`, bg `#fffdf4` | |
| Info | `#5bc0de`, text `#31708f`, bg `#f8fdff` | |

Type scale, not in the instruction block: `h1` 40px · `h2` 24px · `h3` 20px · `h4` 20px · `h5` 16px
· `h6` 14px. Responsive breakpoints: 480 · 768 · 992 · 1200px.

## The gaps

Sixteen classes exist, look like they should work, and don't. `gaps.md` in Knowledge is the full
catalogue — symptom, cause, fix, one section per class. **Search it for the class you are fighting
before concluding you used the class wrong.** The index:

| Class | Symptom | Closed by |
|---|---|---|
| the 28 custom properties | `.side-panel` transparent, focus rings gone | `tokens.css` |
| `color-scheme` | native `<select>` popup and scrollbars stay light in dark | `tokens.css` |
| `.nav-tabs` | renders as a bulleted vertical list | `bundle-fixes.css` |
| `.badge-status-*` | the dot is grey inside a `.list-group-item` | `bundle-fixes.css` |
| `.input-group` | a number and its unit `<select>` sit far apart | `bundle-fixes.css` |
| `.badge-paid` | sits too low beside a label | `bundle-fixes.css` |
| `.avatar` | hangs below the label's baseline in a dropdown | `bundle-fixes.css` |
| `.sp-icon` | the glyph and its label touch | `.margin-right-5` |
| `.badge-status` | text put inside it overflows | don't put text in it |
| `.list-divided` | shows bullets | add `.list-unstyled` |
| `.modal` | invisible, or opens with no backdrop | you supply the JS and the backdrop |
| `.accordion` · `.tab-content` · `.bootstrap-select` | styled but inert — the CSS alone does nothing | your own JS |
| `.settings-toggle-radius` · `.settings-toggle-btn-sm` | the knob sits over the label / on the wrong side | see `gaps.md` |

`tokens.css` and `bundle-fixes.css` between them close seven of the sixteen, which is why both are
shipped and reproduced verbatim. The rest are decisions, argued out in `gaps.md`.

---

## The pre-delivery checklist

The full skill ships three checkers for this — a wiring checker, a class-name checker, and a
Playwright pass over the rendered DOM in both themes. In a chat window you have none of them, so
walk this by hand. It is the same set of assertions, in the order they are worth checking.

- [ ] **Every class name is real.** Search `classes.txt` for each class you used (exact line match)
      and `icons.txt` for each icon name. A miss means *don't use the name* — not "add a rule for
      it". Near-misses are the common failure: `.color-muted-link` exists and `.color-muted` does
      not; `.gap-5` exists and `.gap-xl` does not. Names your code composes at runtime
      (`"badge-status-" + status`) need checking by hand, one value at a time.
- [ ] **Wiring**: the CDN link is present, ahead of app CSS, and never a vendored copy;
      `tokens.css` then `bundle-fixes.css` come after it; app CSS is last; both theme builds are
      linked with one disabled; `ma-light` / `ma-dark` is on `<html>`; no `prefers-color-scheme`
      anywhere in app CSS.
- [ ] **Every `var()` name** in app CSS is one of the 28 in `tokens.css`. Anything else resolves to
      nothing and renders transparent — use the literal value instead.
- [ ] **The frame rules hold**: the app root has no padding, no `max-width`, no `margin: 0 auto`
      and no `overflow`; a screen with a sticky footer sets `height: 100%` (not `100vh`).
- [ ] **Controls are capped one level in** — 364px on the wrapper around each control, 420px or
      540px only where the content needs it, never a cap on the panel or the root, never a `width`
      on `.form-control` itself.
- [ ] **`body` is painted** by the app, and `color-scheme` is declared for both themes.
- [ ] **No theme switcher** anywhere in the UI, and `?theme=` is carried through every URL the app
      builds itself (redirects, OAuth returns, new-tab links) along with `lang` and `access`.
- [ ] **App CSS is short**, and every rule names the bundle gap or design measurement it exists
      for — no colours a semantic class already covers, no re-styled components, no second
      `font-family`, no second icon set.
- [ ] **Restraint holds**: no decorative icons, one primary button per view, one signal per state,
      no panel inside a panel, no `.alert` standing in for a heading. Empty and loading states are
      text first.
- [ ] **Interactive components have behaviour wired up** — the CDN ships no JS, so `.modal`,
      `.dropdown-menu`, `.collapse`, tabs and tooltips do nothing until the app toggles `.open` /
      `.in` / `.active` itself.
- [ ] **The right icon, not just a real one** — the bare plus is `icon-plus-add`, not `icon-plus`.
- [ ] **Checked by eye in both themes.** Tell the user to open the screen with `?theme=dark` too —
      that is the host's own code path, so it also proves the wiring works.

**It is a floor, not a verdict.** A clean pass means nothing is provably wrong, not that the screen
looks right. Spacing, hierarchy and restraint are the part no checklist can judge — say so rather
than calling a screen verified.

## Changing a screen that already exists

Most work is not a new screen, and this changes what the first checklist item means. A shipped
integration carries 15–29 distinct class prefixes of its own, so a name that is not in `classes.txt`
is often that app's own class rather than a mistake.

- **List the app's own prefixes first**, then treat only what remains as findings.
- **Never wave through a prefix the bundle owns** (`color-`, `gap-`, `btn-`, `badge-`): a near-miss
  inside a bundle-owned family is exactly the bug worth catching.
- **Fix what you touch, not what you find.** Pre-existing findings in a screen you are editing are
  not yours to clear; a "while I'm here" rewrite is how a small change becomes unreviewable.
- **On the other delivery route** — an app that gets the design system through its own build — the
  vocabulary is larger, so a name missing from `classes.txt` may be perfectly real there.
