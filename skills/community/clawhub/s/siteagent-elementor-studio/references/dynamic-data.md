# Dynamic data stacks (ACF & Crocoblock/JetEngine) — reference

## Dynamic data stacks — ACF & Crocoblock/JetEngine (Tier-0)

> ⚠️ **Names below are from public docs, UNVERIFIED on a live site.** Treat every
> widget-type string / dynamic-tag id here as a *hint*, not gospel. Before relying
> on one, **discover it at runtime** (list the available widget types / inspect an
> existing element with `get-page-structure`) and **read back the first write** to
> confirm it persisted. This is the same verify-or-bail discipline as the V4
> section — these stacks were detected, not yet exercised end-to-end here.

The setup script / `new-client.sh` report **ACF** and **JetEngine** when active.
Branch on those the way you branch on Pro.

### ACF (Advanced Custom Fields)

ACF is a *data* layer, not widgets. You surface its fields through Elementor's
**Dynamic Tags**, which means **Elementor Pro is required** (free Elementor has no
dynamic tags). If ACF is active but Pro is not, say so and fall back to static
content (or a free dynamic-tag plugin the user installs).

- Bind an ACF field to a widget setting with `set-dynamic-tag` (same tool as the
  Dynamic Tags section), pointing at the ACF source tag + the field name/key.
- The field must be **exposed** — ACF field group saved, and for some flows
  `show_in_rest` enabled — or the tag resolves empty. If a bind reads back empty,
  check the field group before retrying.
- Hint set (confirm at runtime): Elementor Pro registers per-type ACF tags such as
  `acf-text`, `acf-url`, `acf-image`, `acf-number`, `acf-color`, `acf-file`,
  `acf-gallery`, `acf-date-time`, `acf-post-object`. Repeater/flexible-content
  fields are **not** bindable via dynamic tags — use a JetEngine repeater/listing
  or HTML instead.

### Crocoblock / JetEngine

JetEngine registers its own Elementor widgets. There is **no dedicated MCP tool**
for them — place them with the **generic `add-widget`** using the Jet widget's
type string, then set its controls.

- **Discover the exact `widgetType` first.** Either list the available widget types
  the MCP/site exposes, or drop the widget once in the editor and read it back with
  `get-page-structure`. Do **not** hardcode from the hint list below without this.
- Hint set (confirm at runtime): `jet-listing-grid` (dynamic listings),
  `jet-listing-dynamic-field`, `jet-listing-dynamic-image`, `jet-listing-dynamic-link`,
  `jet-listing-dynamic-meta`, `jet-listing-dynamic-repeater`,
  `jet-listing-dynamic-terms`.
- A Listing Grid needs a **Listing Item template** to point at. Creating that
  template, plus CPTs / meta boxes / the Query Builder, are **JetEngine admin-side**
  operations that are **not** drivable through this MCP. If the user needs those
  built, tell them to create the listing/CPT in JetEngine first, then you wire the
  Listing Grid to it.
- After the first `add-widget` of a Jet type, **read it back** — if it didn't
  persist or renders empty, the type string or a required control is wrong; fix
  before repeating.

### What's in scope vs not (Tier-0)

- ✅ In scope: detecting these stacks; binding ACF fields via Pro dynamic tags;
  placing Jet widgets via `add-widget` with runtime-discovered types; read-back.
- ❌ Not in scope: creating ACF field groups, JetEngine CPTs/meta boxes/listings,
  or the Query Builder — those are admin-side. Hand them back to the user.

