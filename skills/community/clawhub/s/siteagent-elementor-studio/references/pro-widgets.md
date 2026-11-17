# Pro-only widgets & features — reference

## Pro-only widgets & features

These sections apply **only when Pro was detected** at the top of the skill. If
the site is Free, these tools are not exposed — use the documented free-tier
patterns instead (Loop Grid → duplicate-element grid; Popups → no equivalent;
Dynamic Tags → static content; Sticky/Motion → Customizer CSS).

> The widget-vs-HTML anti-pattern still applies in full. Pro widgets give you
> *more* native building blocks, which is **more** reason never to dump HTML.

### Loop Grid / Loop Carousel — dynamic listings

`add-loop-grid` (and `add-loop-carousel`) render a repeating template across a
query of posts/CPTs/products — the native, editable replacement for hand-built
card grids when the content is dynamic.

1. **Build the loop item template** — a small Container with the card layout
   (Image → Heading → Text → Button) wired to **Dynamic Tags** (post title,
   featured image, excerpt, permalink) so every item pulls its own data.
2. **Add the Loop Grid** with `add-loop-grid`, point it at that template, and set
   the query (post type, count, order) + columns/gap via the widget's settings.
3. Confirm exact setting keys with `get-widget-schema({ widget_type: "loop-grid" })`
   before building.

Use this for blog feeds, portfolios, team grids, product listings. For a fixed
set of bespoke non-dynamic cards, the `duplicate-element` pattern is still correct.

### Popups

`create-popup` builds a popup template; then configure triggers / conditions /
timing (on load, on scroll %, exit intent, after delay; display conditions for
which pages it shows on).

1. `create-popup` → returns a `post_id`; build the popup content into it with
   native widgets like any page.
2. Set trigger + display rules via the popup's settings (load `get-widget-schema`
   / the popup settings schema to confirm keys).
3. Wire an open action where needed (e.g. a Button's link set to the popup), or
   let the trigger fire it automatically.

### Dynamic Tags

`set-dynamic-tag` binds live data to a widget setting instead of a static value —
post title/excerpt/featured image, author, site name/logo, ACF/custom fields,
archive title, etc.

- Use it to make Theme Builder templates (single/archive) and Loop Grid items
  data-driven.
- Bind on the specific setting (e.g. a Heading's `title`, an Image's `image`) via
  `set-dynamic-tag` pointing at the source tag + its options.

### Sticky header & Motion Effects

These are the Pro-native answer to the free-tier "solid header / Customizer CSS"
note.

- **Transparent-on-top → solid-on-scroll header:** set the header Container's
  **Sticky** to `Top` plus a sticky-state background, instead of hand-writing a
  scroll listener. Configure via the container's sticky/effects settings.
- **Motion Effects** (scrolling/mouse parallax, entrance animations, transforms)
  are exposed as element settings — set them on the target element rather than
  emitting custom JS/CSS.
- Confirm the effects setting keys via `get-container-schema` / the element's
  widget schema before writing them.

