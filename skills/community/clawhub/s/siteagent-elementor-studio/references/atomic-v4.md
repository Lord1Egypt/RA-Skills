# Building on Elementor 4 (atomic / V4) — reference

## Building on Elementor 4 (atomic / V4)

Apply this section **only when you detected the atomic engine** (atomic tools
present). On a classic-engine site, ignore it and use the classic widget tools
everywhere. **Never mix:** classic `add-heading`/`add-container` writes do not
persist on an atomic page, and atomic writes don't belong on a classic page.

### Atomic tool family — use instead of the classic ones

| Need | Classic (don't use on V4) | **Atomic (V4)** |
|---|---|---|
| Flex container | `add-container` | `add-flexbox` *(direction/justify/align/gap/wrap/padding/background_color)* |
| Block container | `add-container` | `add-div-block` |
| Heading | `add-heading` | `add-atomic-heading` |
| Body text | `add-text-editor` | `add-atomic-paragraph` |
| Button | `add-button` | `add-atomic-button` |
| Image | `add-image` | `add-atomic-image` |
| SVG / video / divider | `add-icon` / `add-html` | `add-atomic-svg` / `add-atomic-youtube` / `add-atomic-video` / `add-atomic-divider` |
| Anything else | `add-widget` | `add-atomic-widget` *(any atomic type; pass raw `$$type` settings — correct on every version, see note)* / `update-atomic-widget` |

### The atomic data model (what's different)

- **Typed props (`$$type`).** Atomic settings are typed values, not flat strings.
  For the **dedicated** helper tools (`add-atomic-heading`, `add-atomic-paragraph`,
  `add-atomic-button`, `add-flexbox`, …) the MCP wraps them for you — **pass simple
  flat values** (e.g. `title: "Hello"`, a hex `color`, a `{size,unit}` dimension) and
  it stores them in the `$$type` format Elementor's atomic engine expects.
  **For the universal `add-atomic-widget` / `update-atomic-widget`, always pass raw
  `$$type` values** (fetch the shape with `get-widget-schema`). That is correct on
  every plugin version: since 1.27.0 the save path coerces flat values through
  `Atomic_Props::coerce_tree()`, and already-typed props pass through it untouched —
  whereas on older builds those two tools wrote settings verbatim and a flat value
  was silently saved as empty. Typed values work either way, and the version is not
  always knowable mid-session, so don't make the write depend on it.

  **A direct `_elementor_data` patch has no wrapper on any version.** It bypasses the
  plugin entirely, so every prop must be raw `$$type` there too.
- **Styles live in a separate `styles` map**, not inline on the element. Layout
  props on `add-flexbox` (direction/justify/align/gap) are written as local styles
  automatically — you don't hand-build the styles map.

  **Since plugin 1.28.1, `update-atomic-widget` takes flat style params too**
  (`padding`, `width`, `border_*`, `css_position`, `shadow_*`, typography, …) and
  merges them into the element's base style variant, preserving props it wasn't
  asked to change. Before that it wrote only `settings`, so a padding sent there
  saved, reported success and rendered nothing — which is why older notes say
  delete-and-recreate is the only way to restyle an atomic element. It isn't any
  more. `settings` still means CONTENT.
- **Confirm keys per widget** with `get-widget-schema` before building anything
  non-trivial; the atomic prop names differ from the classic control names.

### How local styles actually attach — `settings.classes` + the `styles` map

This is the wiring the creation helpers (`add-atomic-*` / `add-flexbox` / the universal
`add-atomic-widget`) do for you — and the shape you hand-build only when patching
`_elementor_data` directly. (On plugin **1.28.1+** `update-atomic-widget` also writes the
`styles` map: pass flat style params and it merges them into the element's base variant.
On older builds it could only change which classes `settings.classes` referenced, which is
why the notes below describe recreation or a Global Class as the way to restyle.) An
atomic element carries **two coupled pieces**:

1. **`settings.classes`** — a typed prop listing the class IDs the element wears:
   ```json
   "classes": { "$$type": "classes", "value": ["e-<elementId>-<hash>", "g-1a2b3c4"] }
   ```
   It is a **reference list only** — an id here with no matching style definition renders
   nothing.
2. **`styles`** — a **top-level map on the element** (sibling to `settings`/`elements`),
   keyed by the same class id, holding the actual style definition:
   ```json
   "styles": {
     "e-<elementId>-<hash>": {
       "id": "e-<elementId>-<hash>", "label": "local", "type": "class",
       "variants": [ { "meta": {"breakpoint":"desktop","state":null}, "props": { /* $$type props */ }, "custom_css": null } ]
     }
   }
   ```

**The rule:** every id in `settings.classes.value` must resolve — either to a **local**
style def in this element's `styles` map, or to a **Global Class** `g-` id in the Class
Manager (`apply-global-class` / `create-global-class`). A local id present in `styles`
but missing from `settings.classes` won't apply; an id in `settings.classes` with no
`styles` entry and no matching global class is a dangling reference that styles nothing.
The local `styles` map is **built at element-creation time** by the `add-atomic-*` /
`add-flexbox` helpers (and the universal **`add-atomic-widget`** — *not* the classic
`add-widget`, whose writes don't persist on a V4 page): they auto-compile a local class
from the style props you pass (typography, color, background, …) into the element's
`styles` map and wire its id into `settings.classes` for you. On plugin **1.28.1+** it can
also be written **after** creation, via `update-atomic-widget` — see the note below.

> **Restyling an existing element depends on the plugin version** — read it from
> `server-info` (`plugin_version`); if that tool isn't exposed at all, the site is on
> 1.28.0 or older, since it cannot be disabled on builds that have it.
>
> On **1.28.1+**, `update-atomic-widget` takes flat style params (`padding`, `width`,
> `border_*`, `css_position`, `shadow_*`, typography, …) and merges them into the element's
> base style variant, preserving props it wasn't asked to change and wiring the class into
> `settings.classes`. `settings` still means CONTENT.
>
> ⚠️ On **older builds** it wrote `settings` only and had no way to touch the `styles` map,
> so a padding sent through `settings` saved, reported success and rendered nothing. There,
> restyle by (a) setting the style at creation via the `add-atomic-*` helpers, or (b)
> pointing `settings.classes` at an existing **Global Class** (`apply-global-class` /
> `create-global-class`).
>
> Either way: writing a class id into `settings.classes` with **no** matching global class
> and **no** matching local `styles` entry is a dangling reference that styles nothing.

### Responsive on V4 — variants, not `_tablet`/`_mobile` suffixes

Classic widgets take responsive values as **suffixed keys** (`align_tablet`,
`columns_mobile` — see `../SKILL.md`). Atomic elements do **not**: each style def holds a
**`variants` array**, and a variant's `meta.breakpoint` (`desktop` = base, then `tablet`,
`mobile`, plus any active custom breakpoints) + `meta.state` (`null`/`hover`/`focus`/…)
select when its `props` apply. Author responsive/state styling by adding variants:

- Via **Global Classes**: `create-global-class` / `update-global-class` take a `variants`
  array of `{ breakpoint, state, styles }` — the base (desktop) is the plain `styles` map,
  each extra variant a breakpoint/state override. See `design-system-crud.md`.
- Via **inline local styles**: add another entry to the style def's `variants` array with
  the target `meta.breakpoint`.

The breakpoint set is **not fixed** — it derives from Elementor's active breakpoints, so a
site with custom breakpoints exposes more than `tablet`/`mobile`. Don't hardcode a list;
mirror the breakpoints the site actually defines.

### Build order on V4

Same top-down discipline as classic, with atomic tools:

1. `update-global-colors` + `update-global-typography` (global kit still applies).
2. `create-page` → build the outer layout with `add-flexbox` (section) → inner
   `add-flexbox`/`add-div-block` (boxed content) → atomic widgets inside.
3. Card grids: build one card from atomic widgets, then `duplicate-element` +
   `update-atomic-widget` per copy (same pattern, atomic tools).
4. Verify after each section with `get-page-structure` + curl the front page.

### Pro widgets on V4 — the real limitation

Elementor has **not** shipped atomic equivalents for the Pro widgets yet (Form,
Loop Grid, Nav Menu, Theme Builder parts). On an atomic page they're classic
islands that **may not render**. So when the design needs them:

- **Contact form:** prefer a **Fluent Forms shortcode** dropped via an atomic
  widget (`add-atomic-widget` of a shortcode/HTML type), not the Pro Form widget.
  Flag to the user that the native Pro Form isn't V4-ready.
- **Dynamic listings:** if Loop Grid won't render, fall back to atomic cards built
  from a query you fetch out-of-band (or `wordpress-api-pro`), or accept a classic
  island only if it renders on this build.
- **Header/footer:** Theme Builder still works at the template level; build the
  template body with atomic tools where supported.

> If the user needs heavy Pro-widget functionality **and** doesn't specifically
> need V4, the lowest-friction path is a classic-engine site (turn off the V4
> page experiment under Elementor → Settings → Features). Surface this tradeoff
> rather than silently shipping a page where the form doesn't render.

