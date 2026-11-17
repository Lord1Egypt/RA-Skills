# Elementor 4 design system CRUD — Global Classes, Variables, Interactions

Apply this only on an **atomic (V4) site** (atomic tools present) with the matching
Elementor experiments on. These tools author the *shared design system* — the same
Class Manager / Variables / Interactions an editor user would build by hand — so an
agent can create reusable styling instead of re-styling every element inline.

All three families register **conditionally**. If the tools below aren't in your
`mcp__elementor__elementor-mcp-*` list, the site's engine/experiments don't support
them — fall back to inline atomic local styles (see `atomic-v4.md`).

> **Permissions.** Every *write* here needs `manage_options` (mutating the shared
> design system / kit is site-wide, not per-post). Variable/interaction *reads*
> (`list-variables`, `get-variable`, `list-interactions`) need `edit_posts`;
> interaction tools additionally require `edit_post` on the target page. If a call
> returns a `forbidden` error, the connected app-password user lacks the cap.

---

## 1. Global Classes (reusable style bundles) — Elementor 4 Class Manager

A Global Class is a named, reusable set of styles (a `g-<7hex>` id) you author once and
apply to many atomic elements — the design-system equivalent of a CSS utility class.
Companion read tool: `list-global-classes` (resolves opaque `g-` ids → names + CSS).

| Tool | Does | Key params |
|---|---|---|
| `create-global-class` | Author a new class | `label` (e.g. `"card-base"`), `styles` (CSS-prop→value map), optional `variants` |
| `update-global-class` | Edit in place, **keeps the `g-` id** so bindings survive | `class_id`, any of `label` / `styles` / `variants` |
| `delete-global-class` | Remove by id | `class_id` |
| `apply-global-class` | Bind an existing class to one element | `class_id`, `post_id`, `element_id` |

- **Ergonomic styles.** `styles` is a plain map like `{"color":"#111","padding":24,"font-size":"1.25rem"}`.
  The tool wraps values into Elementor's atomic `$$type` props automatically. Colors
  (`color`, `border-color`, …), sizes (`padding`, `margin`, `width`, `font-size`, …),
  and unitless numbers (`z-index`, `flex-grow`, …) are typed correctly; anything else
  is stored as a string prop.
- **`styles` replaces only the base/desktop variant** on `update-global-class` — other
  variants are kept. `variants` replaces matching breakpoint/state variants (see
  Responsive below). `label` renames without touching styles.
- **`apply-global-class` is idempotent** — re-applying an already-present class is a
  no-op. It appends the `g-` id to the element's `settings.classes`. A **non-atomic**
  element (no `classes` control) is rejected with error code `not_atomic`, and the
  error embeds the element's compact settings schema so you can see what it *is*.
- **Delete does not cascade.** Elementor ignores dangling `g-` references left on
  elements — those elements simply lose that styling, the page isn't rewritten.
- **Cap: 100 classes.** `create-global-class` refuses past the limit
  (`class_limit_reached`) — delete an unused class first.
- **Invalid props are rejected up front.** When a prop name/type isn't valid for the
  atomic style schema, the write returns `invalid_styles` with the rejected props +
  the allowed schema inline — fix and retry in one round trip (see `error-recovery.md`).
- **Not everything maps.** `background-color` is **not** a valid atomic key (atomic
  uses the structured `background` prop) and flex `gap` is the structured
  `layout-direction` prop, so those are deliberately excluded from the ergonomic map —
  passing them yields an honest schema rejection rather than a silent drop.

**When to use:** the design has a repeated visual treatment (cards, section padding,
button variants). Author it once with `create-global-class`, then `apply-global-class`
to each element — one later `update-global-class` restyles them all.

---

## 2. Variables (design tokens) — colors, fonts, sizes

Variables are the atomic *tokens* (a color / font / size) that Global Classes and
atomic styles reference by id — Elementor 4's real design-token layer, stored on the
active kit. Ids look like `e-gv-<hash>`.

| Tool | Does | Notes |
|---|---|---|
| `list-variables` | List active tokens `{id,type,label,value,order}` | excludes soft-deleted |
| `get-variable` | One token by `variable_id` | `not_found` if absent/hidden |
| `create-variable` | New token | `label`, `type` (`color`\|`font`\|`size`), `value` |
| `edit-variable` | Change `label` and/or `value` in place, **keeps the id** | type is fixed |
| `delete-variable` | **Soft-delete** (tombstone, not purged) | reversible |
| `restore-variable` | Bring a soft-deleted token back | **fork-superset capability** |

- **Value rules (validated).** `color` = strict hex (`#RGB` / `#RRGGBB` / `#RRGGBBAA`;
  named colors rejected). `size` = `<number><unit>` (px/em/rem/%/vw/vh/vmin/vmax/ch/pt/pc/ex/fr)
  **or** a CSS-function expression (`clamp()`/`calc()`/`min()`/`max()`/`var()`/`env()`).
  `font` = a font-family name. Labels: no spaces, ≤50 chars, `[A-Za-z0-9_-]` only (the
  label becomes a CSS custom-property name).
- **Size variables are Pro-only.** On a Free site `create-variable type:size` returns
  `requires_pro` (Elementor filters size tokens out on non-Pro — they'd save but never
  render), and such tokens are hidden from list/get. Colors and fonts work on Free.
- **`restore-variable` is a fork superset.** Delete is a reversible tombstone, and
  `restore-variable` returns the token to the active set — the upstream/editor path
  offers no such undo. Restoring an already-active token is a harmless no-op.
- **Uniqueness + cap enforced.** Duplicate labels → `label_not_unique`; the token cap
  → `limit_reached`. Both map to clear errors.

**When to use:** establish brand tokens once (`create-variable` for each brand color /
font), then reference them from Global Classes and atomic styles. This is the V4-native
counterpart to the classic global-kit flow (`update-global-colors` /
`update-global-typography`) — on a V4 site prefer Variables for anything atomic elements
bind to.

---

## 3. Interactions (per-element animations) — scroll / hover / click

An Interaction attaches a scroll/hover/click animation to **one atomic element on one
page** (a trigger + an animation preset). Stored on the element's top-level
`interactions` field, not in `settings`.

| Tool | Does | Notes |
|---|---|---|
| `list-interactions` | List an element's interactions (ergonomic shape) | `post_id`, `element_id` |
| `add-interaction` | Add one animation | ergonomic fields below |
| `edit-interaction` | **Id-addressable in-place edit** | **fork-superset capability** |
| `delete-interaction` | Remove by `interaction_id` | `not_found` if absent |

Ergonomic fields (defaults shown):

- `trigger` — **Free:** `load`, `scrollIn`. **Pro:** `scrollOut`, `hover`, `click`. Default `load`.
- `effect` — `fade` \| `slide` \| `scale`. Default `fade`.
- `type` — `in` \| `out`. Default `in`.
- `direction` — `''` \| `left` \| `right` \| `top` \| `bottom` \| `top-left` \| `top-right` \| `bottom-left` \| `bottom-right`. Default `''`.
- `duration_ms` (default `600`), `delay_ms` (default `0`).
- `easing` — **Free:** `easeIn`. **Pro:** `easeOut`, `easeInOut`, `backIn`, `backInOut`, `backOut`, `linear`. Default `easeIn`.

- **Pro gating is enforced.** A Pro-only trigger/easing on a Free site returns
  `requires_pro` — use a Free value or activate Pro. Unknown values return `invalid_*`.
- **`edit-interaction` is the fork differentiator.** It finds the item by its
  `interaction_id` and patches only the fields you pass, preserving the id and every
  untouched field (including Pro-only nodes the ergonomic shape doesn't model). Use it
  to tweak an existing animation instead of delete-then-add.
- **Ids: temp → canonical.** `add-interaction` writes a `temp-<hex>` id, saves through
  the document (which canonicalizes it to `{post_id}-{element_id}-{hash}`), then
  re-reads to return the canonical id. Address later edits/deletes by that returned id.
- **Cap: 5 per element** (`interaction_limit_reached`). Interactions attach only to
  atomic elements — a non-atomic target returns `not_atomic` with its schema.

**When to use:** the design calls for entrance/scroll motion on a specific element. On
Free, `fade`/`slide`/`scale` `in`/`out` with `load`/`scrollIn` cover most reveals; reach
for Pro triggers/easing only when Pro is detected.

---

## Where this fits vs. the classic kit

- **Classic (V3) site** → these tools aren't registered. Use the classic global-kit
  flow (`update-global-colors` / `update-global-typography`) and inline widget styles.
- **Atomic (V4) site** → Variables + Global Classes are the design-system layer;
  Interactions add motion. Inline atomic local styles (the `styles` map + `settings.classes`,
  see `atomic-v4.md`) are still fine for one-off styling — reach for Global Classes when
  a treatment repeats.
