# Converting a classic (V3) design to the atomic (V4) engine

Use this when you have a classic-engine design (or a page built with classic widgets)
and need to rebuild it on the **atomic / V4** engine. You do **not** "migrate" data —
there is no in-place converter. You **rebuild** the layout with atomic tools on a V4
page. This file is the tool-by-tool map plus the rules that make the rebuild persist.

> **Read `atomic-v4.md` first** for the atomic data model and the `$$type` envelope
> rules — this file cross-references them rather than repeating them.

## The one rule that trips everyone: never mix engines

Classic writes (`add-heading`, `add-container`, `add-button`, …) **do not persist on a
V4 page** — they appear to succeed and then render nothing. Atomic writes don't belong
on a classic page either. So the conversion is not "edit the classic page"; it's
"**build a fresh atomic page** and reproduce the design with atomic tools." Detect the
engine once (atomic tools present ⇒ V4) and commit to one family for the whole page.

## Tool mapping — classic → atomic

| Classic (V3) | **Atomic (V4)** | Notes |
|---|---|---|
| `add-container` (flex) | `add-flexbox` | direction/justify/align/gap/wrap/padding/background_color as flat params |
| `add-container` (block) | `add-div-block` | non-flex block wrapper |
| `add-heading` | `add-atomic-heading` | `title`, `tag` (h1–h6) |
| `add-text-editor` | `add-atomic-paragraph` | body copy |
| `add-button` | `add-atomic-button` | |
| `add-image` | `add-atomic-image` | |
| `add-icon` / SVG | `add-atomic-svg` | |
| `add-video` (YouTube) | `add-atomic-youtube` | writes the `source` prop |
| self-hosted video | `add-atomic-video` | |
| `add-divider` | `add-atomic-divider` | |
| **anything else** | `add-atomic-widget` / `update-atomic-widget` | universal escape hatch — pass raw `$$type` settings (correct on every version) |

Structural tools (`get-page-structure`, `find-element`, `duplicate-element`,
`move-element`, `remove-element`, `reorder-elements`, `update-element`) are engine-neutral
and work on both.

## The `$$type` envelope rule (cross-reference, don't re-derive)

Per `atomic-v4.md`: the **dedicated** atomic helpers (`add-atomic-heading`,
`add-flexbox`, …) take **flat** values and wrap them into `$$type` props for you.

For the **universal** `add-atomic-widget` / `update-atomic-widget`, pass raw `$$type`
values (fetch the shape with `get-widget-schema`). That holds on every plugin version:
since **1.27.0** the save path coerces flat values, and already-typed props pass through
untouched; on **older builds** those tools wrote settings verbatim and flat values were
silently saved as empty. Typed works either way, so don't make the write depend on a
version you may not be able to read mid-session. A direct `_elementor_data` patch never
gets a wrapper on any version.

Prefer the dedicated helpers for everything they cover; use the universal tool only for
atomic types without a helper.

## Styling parity: local styles vs. Global Classes

Classic styling is inline on the widget. Atomic styling lives in a separate `styles`
map referenced by `settings.classes` (see the wiring section in `atomic-v4.md`). Two
ways to reproduce a classic design's look:

1. **Inline atomic local styles** — the dedicated helpers (`add-flexbox` layout props,
   atomic widget style params) build the `styles` map + `settings.classes` for you. Best
   for one-off, per-element styling — the direct analog of classic inline settings.
2. **Global Classes** — when the classic design repeats a treatment (every card, every
   section's padding), author it once with `create-global-class` and `apply-global-class`
   to each element. This has no clean classic equivalent and is the better V4 result —
   editable in one place. See `design-system-crud.md`.

For brand tokens, prefer V4 **Variables** (`create-variable`) over ad-hoc hex/font, so
atomic styles bind by token. (`design-system-crud.md`.)

## Worked example — a classic hero → atomic

Classic build (V3):

```
add-container(settings:{flex_direction:"column", flex_align_items:"center", min_height:{unit:"vh",size:100}, ...})
  └─ add-heading(title:"Where estates <em>are entrusted</em>", header_size:"h1", title_color:"#fff", ...)
  └─ add-text-editor(...)
  └─ add-button(text:"Book a consultation", ...)
```

Atomic rebuild (V4) — same tree, atomic tools, flat values on the dedicated helpers:

```
add-flexbox(post_id, parent_id, direction:"column", align:"center", ...)   → returns hero_id
  add-atomic-heading(post_id, parent_id: hero_id, title:"Where estates <em>are entrusted</em>", tag:"h1")
  add-atomic-paragraph(post_id, parent_id: hero_id, content:"...")   # param is `content` (mapped to the e-paragraph `paragraph` prop internally)
  add-atomic-button(post_id, parent_id: hero_id, text:"Book a consultation")
```

Then style:

- **Repeated treatment?** e.g. every hero on the site shares padding + max-width →
  `create-global-class(label:"hero-shell", styles:{padding:"96px", "max-width":"1360px"})`
  then `apply-global-class(class_id, post_id, element_id: hero_id)`.
- **One-off?** pass the style params on the dedicated helper (they build the local
  `styles` map for you) **at creation**. For an atomic type without a dedicated helper,
  create it with the universal **`add-atomic-widget`**, or apply an existing/new **Global
  Class**. To restyle an element that already exists, `update-atomic-widget` takes flat
  style params on plugin **1.28.1+** and merges them into the base variant; on **older
  builds** it merged `settings` only and could not write the `styles` map, so a style param
  sent there became an ordinary `settings` key that Elementor ignores: saved, reported
  successful, rendered nothing. (That is a different failure from a **dangling class
  reference**, which is what you get by writing a class id into `settings.classes` with no
  matching local `styles` entry and no matching Global Class.)
- **Responsive?** classic used `_tablet` / `_mobile` suffix keys; V4 uses **variants**
  with a `breakpoint` (`create-global-class` `variants`, or the styles-map variant meta).
  See the Responsive sections in `../SKILL.md` and `atomic-v4.md`.
- **Motion?** a classic entrance animation becomes an **Interaction**
  (`add-interaction`, e.g. `trigger:"scrollIn", effect:"fade", type:"in"`).

## Conversion checklist

1. Confirm the target is a V4 page (atomic tools present). If the user only wants the
   look and not V4 specifically, a classic-engine rebuild is lower-friction (Pro widgets
   render) — surface that tradeoff (see `atomic-v4.md` "Pro widgets on V4").
2. Rebuild the **structure** top-down with `add-flexbox` / `add-div-block`, keeping the
   classic tree shape. Grab each returned `element_id`.
3. Place **content** with the dedicated atomic widget helpers (flat values).
4. Reproduce **styling** — Global Classes + Variables for anything that repeats, inline
   local styles for one-offs.
5. Re-add **responsive** as variants and **motion** as Interactions.
6. Verify after each section: `get-page-structure` + curl the rendered page. Atomic
   silently drops invalid props, so *look at the result*, don't assume.
