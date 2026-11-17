---
name: siteagent-elementor-studio
version: 1.7.1
license: MIT
description: Helps with WordPress + Elementor work via the elementor-mcp MCP server — building new pages, editing existing ones, inspecting site state, or exploring what's possible. Auto-detects Elementor Pro (native Form, Theme Builder, Loop Grid, Popups, Dynamic Tags, Sticky/Motion vs free-tier workarounds) AND the page engine (classic vs Elementor 4 atomic/V4 — atomic uses add-flexbox/add-atomic-* tools since classic writes don't persist on a V4 page). Detects ACF + Crocoblock/JetEngine for dynamic-data binding (Tier-0; bind ACF via Pro dynamic tags, place Jet widgets via add-widget with runtime-verified types). On atomic (V4) sites, authors the Elementor 4 design system — Global Classes, Variables (design tokens), and per-element Interactions — and recovers from the fork's schema-in-error and governance responses. Asks what the user wants before acting. Use when the user references the Elementor MCP, invokes `/siteagent-elementor-studio`, or runs `mcp__elementor__elementor-mcp-*` tools. Also covers initial install of the MCP Adapter + elementor-mcp plugins, app-password auth wiring, schema-loading discipline, and the widget-vs-HTML decision tree. SKIP for Bricks, Divi, Beaver Builder, or non-Elementor WordPress builds.
permissions:
  shell: "Runs the bundled setup script (files/setup-elementor-mcp.sh) — only on explicit user confirmation. It shells out to curl/unzip/zip/python3 and, for Local sites, drives Local by Flywheel's bundled WP-CLI (plugin install/activate) against the running site's PHP + MySQL socket."
  network:
    - "GitHub release download over HTTPS from the trusted Digitizers/elementor-mcp repo (api.github.com + release asset host) — the elementor-mcp plugin zip. By default the release this kit pins (EMCP_DEFAULT_VERSION in the setup script), checked before it is unpacked or installed against the sha256 recorded beside the pin — out of band from the download. EMCP_PIN_VERSION=<tag> or =latest selects another release, checked against the digest that release publishes (integrity, not provenance) or EMCP_EXPECTED_SHA256. Nothing is installed unverified"
    - "The target WordPress site's REST API (/wp-json/ — auth check, plugin list/install, MCP route verification). Plaintext http:// is refused for a non-local host unless that exact host is named in WP_ALLOW_HTTP, because the run sends a reusable application password on every request"
  filesystem:
    - "Writes .mcp.json in the current working directory, created mode 600 before the credential is written (it embeds a reusable Basic-Auth WordPress credential), and appends .mcp.json to .gitignore there"
    - "Reads Local by Flywheel site paths + bundled WP-CLI/PHP binaries; creates a temp working dir for the plugin zip"
  env:
    - "WP_URL / WP_USERNAME / WP_APP_PASSWORD (when used to supply the target site + Application Password auth)"
    - "EMCP_PIN_VERSION (optional — a release tag, or latest, instead of the release this kit pins; the kit's pin never downgrades an installed newer plugin — the run stops and names this override)"
    - "EMCP_EXPECTED_SHA256 (optional — verify the plugin zip against a digest obtained out of band; required for a release that publishes no digest)"
    - "WP_ALLOW_HTTP (comma-separated host list — permits plaintext http for exactly those hosts; a blanket value is not a hostname and permits nothing)"
---

# SiteAgent Elementor Studio Skill

You are operating against a WordPress site with the **elementor-mcp** server (`https://github.com/Digitizers/elementor-mcp` — our fork, Elementor 4.x-correct) connected via the WordPress MCP Adapter. This skill captures everything I learned the hard way the first time through, so subsequent sessions start at expertise level.

## 🛑 First Action Protocol — ASK BEFORE DOING

**When this skill is invoked, do not start running tools. Ask the user what they want first.**

> **Shell / setup actions run only on explicit user confirmation.** The bundled `setup-elementor-mcp.sh` (which shells out, runs Local's WP-CLI, downloads the plugin, and writes a credentialed `.mcp.json`) is never run automatically — offer it and wait for the user to say yes.

If the user's invocation message *already* contains a clear task — *"build me a hero section from `index.html`"*, *"show me my current global colors"*, *"change the burgundy to navy"* — proceed with that task directly.

Otherwise *(invocations like `/siteagent-elementor-studio` alone, or "use the Elementor MCP" with no follow-up)*, **respond with this menu and wait for the user to pick:**

```
What would you like to do with your Elementor site?

  1. Build       — create new pages or sections from a design
  2. Edit        — change something on an existing page
  3. Reference   — inspect current state (pages, colors, fonts, content)
  4. Explore     — show me what's possible / what can the MCP do here
```

Do **not** silently default to "build" — that's the most destructive action and forces a path the user may not want. Wait for the user to choose 1/2/3/4 *(or describe their task in their own words)* before invoking any MCP tool other than the harmless read-only ones at the bottom of this section.

### Read-only "smoke test" calls that are always safe to run

When the user picks any option, you can run these **before** asking follow-up questions, since they help frame the next response:

- `mcp__elementor__elementor-mcp-list-pages` — confirms auth + lists what's there
- `mcp__elementor__elementor-mcp-get-global-settings` — current colors/fonts kit

That's it for unprompted tool calls. **Anything that creates, modifies, or deletes data requires the user to have explicitly asked for it.**

## When this skill applies

- The user mentions Elementor MCP, types `/siteagent-elementor-studio`, or says "use the Elementor MCP"
- A `.mcp.json` in the project registers an MCP server pointing at `wp-json/mcp/elementor-mcp-server`
- The user asks to build, edit, inspect, or troubleshoot an Elementor page
- Tools beginning with `mcp__elementor__elementor-mcp-*` are available

## First-session setup (when MCP not yet connected)

> **Engine:** this skill drives our fork `Digitizers/elementor-mcp` (v1.34.1, the release this kit's installer pins; Elementor 4.x-correct), a single self-contained plugin — no Freemius, no phone-home. Since fork v1.28.0 it carries its own update checker, which **offers** later GitHub Releases on the site's normal Updates screens (release-only, a user agent naming only the plugin); installing one is WordPress's ordinary update flow, and the fork does not switch on WordPress's per-plugin auto-update. **Never run it alongside the paid "MCP Tools for Elementor (Premium)" — same class names → fatal.** Details + switch commands → `references/engine-and-premium.md`.

If the user has a WordPress site but no **working** `elementor` MCP connection — either no `.mcp.json` at all, or only this kit's committed placeholder config (values like `"WP_URL": "${WP_URL:-}"` with those env vars unset) and no `mcp__elementor__elementor-mcp-*` tools loaded:

> In the placeholder case there are two fixes, not one: **export `WP_URL` / `WP_USERNAME` / `WP_APP_PASSWORD`** (the committed config reads them — fastest in this repo's checkout or a cloud session), or run the wizard below from a **separate per-site project directory** (it refuses to write credentials into the tracked placeholder file).

1. **Check whether they're using Local-by-Flywheel or a live host.** Setup paths differ.
2. **Run the bundled setup script** from the loaded skill's directory — it handles plugin install, auth wiring, and `.mcp.json` generation interactively for both flavors. The skill's base directory is announced when this skill loads (look for the filesystem path in the skill load message). Replace `<skill-dir>` with that announced path:
   ```bash
   bash "<skill-dir>/setup-elementor-mcp.sh"
   ```
   Keep the quotes — plugin-cache paths can contain spaces (e.g. a Windows
   profile named `First Last`), and an unquoted substitution splits the path.
   **If `<skill-dir>/setup-elementor-mcp.sh` is not found** (e.g., from a manual `INSTALL.sh` run instead of plugin-marketplace), use the fallback path for manual installations:
   ```bash
   bash ~/.claude/scripts/setup-elementor-mcp.sh
   ```
3. After the script completes, instruct the user to **quit and reopen Claude Code in the project directory** so the new `.mcp.json` is picked up.
4. On reopen, the deferred MCP tools will be exposed via ToolSearch — load the ones you need with `select:` queries.

If something fails, see "Setup gotchas" below.

## Working session conventions

### Always do this first

```
mcp__elementor__elementor-mcp-list-pages   # confirms auth + lists existing pages
mcp__elementor__elementor-mcp-get-global-settings   # see existing colors/fonts kit
mcp__elementor__elementor-mcp-get-container-schema  # ground truth on flex_* key names
```

### 🎯 Detect Pro vs Free FIRST — it changes which path you take

Before building anything, determine whether **Elementor Pro** is active. The
whole skill branches on this: with Pro you use native widgets (Form, Theme
Builder, Loop Grid, Popups, Dynamic Tags, Sticky/Motion); without it you use the
free-tier workarounds documented further down (Fluent Forms, UAE/HFE, HTML for
motion).

**How to detect — by tool availability (the definitive Pro signal):**

The elementor-mcp server exposes Pro tools **conditionally**. When Pro is active
the tool list grows from ~74 to ~100+ tools and Pro-only tools appear. Check
whether these exist in your available `mcp__elementor__elementor-mcp-*` tools:

- `add-form` — present ⇒ **Pro active**
- `create-theme-template` — present ⇒ **Pro active**
- `add-loop-grid` / `add-loop-carousel` — present ⇒ **Pro active**
- `create-popup`, `set-dynamic-tag` — present ⇒ **Pro active**

If none of those Pro tools are exposed, treat the site as **Free** and use the
workarounds. The **tool-presence check above is the definitive Pro-vs-Free
signal** — prefer it. (`detect-elementor-version` is reliable on current builds —
the old v1.5.0 schema bug is fixed — but it reports **atomic/version** support,
not a Pro flag, so it doesn't settle Pro-vs-Free on its own.)

> **Record the verdict once** ("Pro detected" / "Free only") and state it to the
> user up front, then follow the matching branch in every section below. Each
> "Forms", "Header/Footer", and motion section is written as **If Pro → … /
> If Free → …**. Don't mix paths.

### 🧬 Also detect the ENGINE — classic vs atomic (Elementor 4 / V4)

There's a **second** axis that changes everything: the page engine. Elementor 4
introduced the **atomic / V4** engine (`e-flexbox`, `e-div-block`, atomic
widgets, a typed-prop `$$type` data model). Classic widget writes **do not
persist on an atomic page** — they silently appear to do nothing. So before
building, decide classic vs atomic.

**How to detect — by atomic tool availability (preferred):**

The atomic tools register only when the site is on the atomic engine. Check your
available tools:

- `add-flexbox`, `add-div-block`, `add-atomic-heading` / `add-atomic-button` / …,
  `add-atomic-widget` / `update-atomic-widget` present ⇒ **atomic (V4) engine**
- Only classic `add-container` / `add-heading` / … present ⇒ **classic engine**

You may also call `detect-elementor-version` (reliable on current releases — it
returns whether atomic is supported). The old v1.5.0 schema bug is fixed; still,
tool-presence is the most direct signal.

> **Which elementor-mcp PLUGIN version am I on?** Some behaviour below branches on
> it, and `detect-elementor-version` answers about *Elementor*, not the plugin.
> Call **`server-info`**: it returns `plugin_version` (plus registered-vs-exposed
> tool counts and what is withholding the rest). It is always registered and
> cannot be disabled, so **its absence is itself the answer** — no `server-info`
> means the site is on **1.28.0 or older**. Use it for the one branch that needs it —
> whether `update-atomic-widget` can restyle in place (1.28.1+). Nothing else should
> depend on the version: for the universal atomic tools, pass raw `$$type` values, which
> are correct on every build.

> ⚠️ **Antigravity / tight tool caps.** Antigravity caps MCP tools at ~100. The
> full Pro+atomic set is ~113, so atomic tools can get truncated and never reach
> the client — making a V4 site look like "writes don't persist". Fix: enable the
> MCP plugin's **Low-tools mode** (WP Admin → MCP Tools screen). Its curated
> essentials set **includes the 5 atomic essentials** (`detect-elementor-version`,
> `add-atomic-widget`, `update-atomic-widget`, `add-flexbox`, `add-div-block`) and
> stays under the cap.

> 🐞 **Known root cause (older MCP builds).** Elementor often runs atomic as an
> opt-in *experiment* while `ELEMENTOR_VERSION` still reads `3.x`. MCP builds that
> gate atomic on `version_compare(ELEMENTOR_VERSION,'4.0.0','>=')` therefore never
> register the atomic tools on those sites. Fixed upstream by detecting via the
> experiment/module. If atomic tools are missing on a clearly-V4 site, update the
> elementor-mcp plugin (or confirm the V4 experiment is on under Elementor →
> Settings → Features).

Record **both** axes: e.g. "Pro + atomic", "Pro + classic", "Free + classic".
The Pro/Free axis picks Form vs Fluent Forms etc.; the engine axis picks classic
vs atomic widget tools (next section).

The container schema is large (~50KB). Read it once, then write down the keys you'll use in your reply text so you don't need to re-fetch it. Critical keys:

- `flex_direction`, `flex_justify_content`, `flex_align_items`, `flex_gap`, `flex_wrap` — note the **`flex_` prefix** on justify/align (issue #32 was about these being written under wrong keys in older versions)
- `content_width: "boxed"|"full"` + `boxed_width: {unit, size, sizes}`
- `min_height: {unit, size, sizes}` — use unit `vh` for full-screen heroes
- `padding`/`margin: {unit, top, right, bottom, left, isLinked}` — `isLinked: false` when sides differ
- `background_background: "classic"|"gradient"|"video"` — must be set first or other background_* keys are ignored
- `background_overlay_*` — separate parallel set for overlays. `background_overlay_opacity: {unit:"px", size: 0.5}` (yes, the unit is `px` even for opacity — quirk of the schema)

### Widget call convention — flat params, NOT nested in `settings`

This bit me hard the first time. The `add-*` shortcut tools take their settings as **top-level parameters**, not inside a `settings: {}` object:

```js
// ✓ CORRECT
mcp__elementor__elementor-mcp-add-heading({
  post_id: 11,
  parent_id: "abc123",
  title: "where estates <em>are entrusted</em>",
  header_size: "h1",
  title_color: "#FFFFFF",
  typography_typography: "custom",       // ← required to enable typography
  typography_font_family: "Cormorant Garamond",
  typography_font_size: {size: 110, unit: "px"},
  typography_font_weight: "300",
  typography_line_height: {size: 0.98, unit: "em"},
})

// ✗ WRONG — silently fails or returns "title is required"
mcp__elementor__elementor-mcp-add-heading({
  post_id: 11,
  parent_id: "abc123",
  settings: {title: "...", typography_font_family: "..."}
})
```

`add-container` is the **exception** — it takes a `settings: {}` object. Don't generalize from one to the other.

### Always set `typography_typography: "custom"`

Without this, the other typography_* keys are ignored. Same applies to `css_filters_css_filter: "custom"` for image filters, etc. — these "enable" flags are how Elementor knows you want to override defaults.

### Italic emphasis pattern

Display headings often need a single italic-emphasized word. Don't use a separate widget — just inline `<em>` in the title:

```js
title: "A <em>quiet</em> practice for an <em>uncommon</em> clientele."
```

Cormorant Garamond and most luxury serifs have italic variants that auto-load when `<em>` appears. Confirm via the rendered page; if italics fail, the global typography needs the italic variant explicitly enabled.

### Responsive values — suffix keys (classic) vs. variants (atomic)

Elementor stores a responsive control's per-breakpoint values under **suffixed keys**.
The base (desktop) value has **no suffix**; each breakpoint appends its own suffix to the
**same base control key**, with the **same value shape** as desktop:

```js
// classic widget — tablet/mobile overrides of the same control:
mcp__elementor__elementor-mcp-add-heading({
  post_id, parent_id,
  title: "...",
  typography_font_size: {size: 110, unit: "px"},          // desktop (base, no suffix)
  typography_font_size_tablet: {size: 72, unit: "px"},    // tablet
  typography_font_size_mobile: {size: 44, unit: "px"},    // mobile
  align: "left", align_tablet: "center",                  // alignment per breakpoint
})
```

**The suffix set is breakpoint-dependent — do NOT hardcode an incomplete list.** It
derives from Elementor's **active breakpoints** (`add_responsive_control()`), so beyond
`_tablet` / `_mobile` a site may expose `_widescreen`, `_laptop`, `_tablet_extra`,
`_mobile_extra`, or custom ones. Read the site's breakpoints rather than assuming; the
fork passes any `<base>_<breakpoint>` key through as long as `<base>` is a real control.

> **Atomic (V4) is different — no suffix keys.** On a V4 page responsive lives in a style
> definition's **`variants` array**, keyed by a `breakpoint` meta (`desktop` = base, then
> `tablet`/`mobile`/custom) — Global Classes take a `variants` param, local styles add
> variant entries. Never put `_tablet`/`_mobile` suffix keys on atomic elements. See
> `references/atomic-v4.md` and `references/design-system-crud.md`.

## The widget-vs-HTML decision — DEFAULT TO NATIVE WIDGETS

> 🚨 **CRITICAL ANTI-PATTERN — read this first.**
>
> **Do NOT paste an entire HTML page into one HTML widget.** Do NOT build a homepage that is "1 container with 3 HTML widgets inside." That is not building with Elementor — that is using Elementor as a wrapper around a static webpage. The user **cannot edit it** in the Elementor visual editor, **cannot reuse the design tokens**, and **cannot iterate** on it without going back to source code.
>
> If you find yourself thinking *"I'll just dump this section as HTML, it's faster,"* **STOP.** Break it into native widgets.

### Always default to native widgets

For every section the user wants, build it from native Elementor widgets:

- **Headings** → `add-heading` widget *(supports inline `<em>` for italic emphasis)*
- **Body copy** → `add-text-editor` widget
- **Images** → `add-image` widget *(NOT an `<img>` tag inside an HTML widget)*
- **Buttons / CTAs** → `add-button` widget *(NOT an `<a>` styled as a button)*
- **Layout / spacing** → `add-container` with proper `flex_*` settings *(NOT `<div>`s with CSS flex)*
- **Lists** → `add-icon-list` widget
- **Tabs** → `add-tabs` widget
- **Accordions / FAQs** → `add-accordion` widget
- **Forms** → Fluent Forms shortcode via `add-shortcode` widget
- **Nav menu in headers** → UAE Nav Menu widget *(`uael-nav-menu`)*

### When HTML widget IS allowed *(narrow list — exceptions only)*

Only reach for an HTML widget in these specific cases. **Anything not on this list goes through native widgets.**

1. **Tab/accordion content with rich layout.** `add-tabs` only accepts `tab_content` as a string of HTML, so a multi-card grid inside a tab MUST be HTML. *(But the wrapping Tabs widget itself is still native.)*
2. **Decorative-only flourishes** with no native equivalent — a thin gold rule with a CSS-pseudo-element flourish, an animated underline that grows on hover, a gradient overlay on a child element. **Even then, prefer to pair it with a native widget rather than replacing one.**
3. **Form HTML as a flagged placeholder** when no real form plugin is wired up yet — and you must explicitly tell the user "form is visual only, doesn't capture submissions."
4. **Site-wide CSS overrides** scoped to a specific Elementor element ID *(e.g., styling the tab strip of an `add-tabs` widget that the widget controls don't expose)*. These should be small style blocks, not whole sections of markup.

### What about card grids of 4+ items?

Earlier versions of this skill said "use one HTML widget for card grids — it's faster than 50 widget calls." That advice was wrong because it led to non-editable pages.

**The correct path for card grids:**

- Build the first card with native widgets *(Container → Image → Heading → Text Editor → Button)*
- Use `duplicate-element` to copy it 3+ more times
- Use `update-element` to change the copy/image on each duplicate
- Wrap them in a parent Container with `flex_direction: row` and `flex_wrap: wrap`

This is more widget calls, yes, but the result is a **real Elementor card grid** the user can edit, restyle globally, or reuse as a template.

> **If Pro is active and the cards are driven by posts/CPT/products** (a blog feed, portfolio, listings), prefer the native **Loop Grid** (`add-loop-grid`) instead — see the Loop Grid section below. The duplicate-element pattern is still the right answer for a fixed set of bespoke, non-dynamic cards on either tier.

### Cross-widget styling — `<style>`-only HTML widgets

When you need to style a native widget from outside (e.g., overriding the Tabs widget tab strip styles that the widget controls don't expose), use a **`<style>`-only HTML widget**: it contains ONLY a `<style>` block — no markup, no rendered content. Scope every selector to the parent Elementor element ID:

```html
<style>
.elementor-element-f8d1545 .elementor-tab-title {
  text-transform: uppercase !important;
  letter-spacing: .26em !important;
}
.elementor-element-f8d1545 .elementor-tab-title.elementor-active {
  border-bottom-color: #171615 !important;
}
</style>
```

The `f8d1545` is the `element_id` returned when you created the tabs widget. Always grab and remember these IDs — they're the only stable selector across page reloads.

> ⚠️ **An HTML widget used for cross-widget styling MUST contain only `<style>`.** If you find yourself adding HTML markup *(divs, anchors, spans with text content)* alongside the style block, you're falling back into the anti-pattern at the top of this section. Stop. That markup belongs in native widgets.

## Building on Elementor 4 (atomic / V4)

Elementor 4 uses an atomic/V4 data model — classic widget writes don't persist on a V4 page. Detect the engine first (see core detection above), then use the atomic tool family. **Full atomic model, tool family, and build order → load `references/atomic-v4.md`.**

> **Atomic local styles wiring.** Atomic styling attaches through **two coupled pieces** —
> `settings.classes` (a typed list of class ids the element wears) **and** a separate
> top-level `styles` map holding each class's definition. Every id in `settings.classes`
> must resolve to a local `styles` entry or a Global Class `g-` id, or it styles nothing.
> The dedicated helpers build the local `styles` map for you **at creation**. To restyle an
> element that already exists (check the plugin version with `server-info` — absent means
> ≤1.28.0): on plugin **1.28.1+** pass flat style params to
> `update-atomic-widget` and it merges them into the base variant; on **older builds** it
> merged `settings` only and could not write the `styles` map, so restyle there by
> (re)creating with a style-capable helper / universal `add-atomic-widget`, or point
> `settings.classes` at a Global Class. Full pattern → `references/atomic-v4.md`.

### Converting a classic (V3) design to atomic (V4)

There's no in-place migrator — you **rebuild** the design on a fresh V4 page with atomic
tools (classic/atomic never mix). Tool map, `$$type` rules, styling parity, and a worked
example → **load `references/v3-to-v4-conversion.md`.**

## Elementor 4 design system — Global Classes, Variables, Interactions (v1.14+)

On an **atomic (V4)** site the fork exposes CRUD for the shared design system, so you can
author reusable styling instead of re-styling every element:

- **Global Classes** (reusable style bundles): `create-global-class`, `update-global-class`,
  `delete-global-class`, `apply-global-class` (+ read `list-global-classes`).
- **Variables** (color/font/size design tokens): `list-variables`, `get-variable`,
  `create-variable`, `edit-variable`, `delete-variable`, `restore-variable`.
- **Interactions** (per-element scroll/hover/click animations): `list-interactions`,
  `add-interaction`, `edit-interaction`, `delete-interaction`.

`restore-variable` (undo a soft-deleted token) and `edit-interaction` (id-addressable
in-place animation edit) are **fork-superset** capabilities the editor path doesn't offer.
All writes need `manage_options`; these tools register only when the atomic engine +
matching experiments are on. **Full tool shapes, params, Pro gating, caps, and when to use
each → load `references/design-system-crud.md`.**

## When a write fails — errors & recovery

The fork's errors are built for self-correction; read them, don't just relay them:

- **Wrong widget name** → `invalid_widget_type` / `widget_not_found` carry `Did you mean:`
  suggestions **inline in the message** — pick the nearest and retry (no second lookup).
- **Bad atomic settings** → `save_rejected` embeds the atomic type's **prop schema** inline
  — correct the settings and retry in one round trip.
- **Numeric/slider values** → `get-widget-schema` now returns `minimum`/`maximum`/`multipleOf`
  and slider `unit` enums — clamp to them before writing.
- **Governance (opt-in, only with the SiteAgent worker):** `governance_grant_required` /
  `governance_grant_invalid` mean the write needs a gateway-minted approval grant (you can't
  self-fix — the user must approve); `governance_render_failed` means the write broke the page
  and **was reverted** (don't blindly re-send — fix the cause); `governance_rollback_failed`
  means the revert itself failed and the page may be **partially written** — **stop and
  escalate** with the snapshot id.

**Full recovery playbook (all error codes, retry semantics, range hints) → load
`references/error-recovery.md`.**

## Brand kit — intake & tokens

Triggers when the user is setting up a new client / brand, or says "set up the
brand". Establishes the design tokens every later build references **by name, never
raw hex/font**. Full schema + tool shapes: [`references/brand-kit.md`](references/brand-kit.md).

The 8 color tokens (`brand, accent, heading, text, bg, surface, muted, border`) and
2 font tokens (`heading-font, body-font`) map to **named Elementor custom globals**.

Flow:

1. **Gather** the brand — 8 colors (hex), 2 font families, logo — from the user's
   brief, a Figma file, or by asking. If fewer than 8 colors are given, derive the
   rest (`surface` = tint of `bg`; `muted` = lower-contrast `text`; `border` = light
   grey) and state the derivation.
2. **Apply** — `update-global-colors` with the 8 `{_id, title, color}` entries, then
   `update-global-typography` with the 2 font entries. (Exact payloads in the
   reference.)
3. **Record** the token→value map back to the user so recipes and later edits reuse it.
4. **Verify** — `get-global-settings` shows the 8 colors + 2 fonts by name.

After intake, **bind widget colors to these globals** (or use the recorded token
value when setting directly). Introducing an ad-hoc hex/font mid-build breaks brand
consistency — don't.

## Recipe library

Reusable, brand-token-driven build sequences for common sections. **Before building a
section, consult the matching recipe** and bind everything to the brand tokens (see
"Brand kit" above). Classic-first; apply the recipe's Pro/V4 variant note when those
engines are active. Full trees + token bindings: [`references/recipes.md`](references/recipes.md).

Available recipes: **Hero**, **Services grid**, **Split (image + text)**, **Stats
band**, **Testimonials**, **CTA band**, **Contact**, **FAQ**, **Pricing**, **Logos
strip**. (The library grows — add a recipe when a new section type recurs.)

Recipes reuse the rest of this skill's rules (native widgets not HTML dumps,
`duplicate-element`/Loop Grid for grids, flat-param convention) — they don't restate
them.

## When the user asks to BUILD — building order

**Studio voice default:** clean, confident, conversion-focused; real copy (no lorem); accessible contrast; consistent spacing scale. Per-client tone comes from the matched vertical (see `references/verticals/`).

**Vertical routing:** if the client matches a known vertical, load its pack first for voice + design system + section flow: `references/verticals/{dental,salon,car-wash,local-business,portfolio}.md`. No match → proceed with the studio voice default + the recipe library.

> Use this section only when the user has explicitly asked you to build something. Do not run this flow on a bare `/siteagent-elementor-studio` invocation.

For a new page, build top-down section by section, in small commits, verifying after each:

1. **Brand kit** — if the brand tokens aren't set yet, run the brand-kit intake flow (see "Brand kit — intake & tokens" above) to establish the named global colors/typography. If already set, confirm via `get-global-settings`.
2. `create-page({title, status: "publish", template: "elementor_canvas"})` — Canvas template removes theme header/footer chrome so your design is the only thing on the page
3. (Via WP-CLI) Set as static front page: `wp option update show_on_front page; wp option update page_on_front <id>`
4. Build sections — **use the matching recipe from the Recipe library** (outer container → inner boxed container, max-width ~1360px → content), bound to brand tokens
5. After each section: `get-page-structure(post_id)` to verify nesting, or just curl the front page
6. **Pause for human review** before building header/footer (which use Header Footer Elementor templates, a different flow)

## When the user asks to EDIT

Approach existing pages surgically — don't rebuild what you don't have to:

1. `list-pages` to find the page they're editing
2. `get-page-structure(post_id)` to see the current widget tree and grab element IDs
3. For a specific element they describe ("the hero headline", "the third listing card"), use `find-element` if needed, then `update-element` with only the fields that change
4. Verify the edit by re-reading `get-page-structure` or curling the rendered page
5. **Never delete a section unless they explicitly ask** — even when restructuring. Use `move-element` or `update-element` first.

## When the user asks to REFERENCE / INSPECT

Read-only tools, no writes. Useful for "show me", "tell me", "what's", "list" requests:

- `list-pages` — what pages exist
- `get-global-settings` — colors, typography, layout settings
- `get-page-structure(post_id)` — what's on a page
- `get-element-settings(element_id)` — exact settings of one widget
- `find-element(post_id, ...)` — locate a widget by content/type

Format the response as a clear summary, not a JSON dump. The user wants understanding, not raw data.

## When the user asks to EXPLORE / "what can you do?"

Give a short menu *(don't dump the whole tool list)*. Point them at the four modes from the First Action Protocol with concrete examples:

- *"Build a homepage from this HTML mockup"* → mode 1
- *"Make the hero text 20% smaller"* → mode 2
- *"Show me what colors are currently set globally"* → mode 3
- *"What pages exist on the site?"* → mode 3

Then ask which mode they want.

## Header/Footer notes

Theme Builder (Pro) is the preferred header/footer path; UAE/HFE is the free fallback. **Full patterns (Theme Builder vs UAE/HFE, nav menu, site-wide header/footer) → load `references/header-footer.md`.**
## Pro-only widgets & features

When Pro is active, native widgets beat HTML: Loop Grid/Carousel, Popups, Dynamic Tags, Sticky header + Motion Effects. **Full per-feature guidance → load `references/pro-widgets.md`.**
## Dynamic data stacks — ACF & Crocoblock/JetEngine (Tier-0)

Bind ACF via Pro dynamic tags; place Jet widgets via `add-widget` with runtime-verified types. Tier-0 scope only. **Full ACF + Crocoblock/JetEngine guidance → load `references/dynamic-data.md`.**
## Forms

If Pro → native Form widget (preferred). If free → Fluent Forms (fallback). **Full form guidance (native Form settings, Fluent Forms class map, alternatives) → load `references/forms.md`.**
## Setup gotchas (what bit me last time)

- **The application password's *label* is not the username.** A user creates an Application Password and gives it a name like "Claude MCP", but the actual WP username remains `admin` or `test` or whatever they set up. If `curl -u "ClaudeMCP:..."` returns 401, try `curl -u "admin:..."` or check `GET /wp-json/wp/v2/users` to find the real slug.
- **Local-by-Flywheel `wp-config.php` says `DB_HOST=localhost`** but the real MySQL is on a per-site Unix socket. WP-CLI fails with "Error establishing a database connection" until you pass `-d mysqli.default_socket=/path/to/mysqld.sock`. The setup script handles this; if doing it manually, find the socket via `find ~/Library/Application\ Support/Local/run -name mysqld.sock`.
- **Neither MCP plugin is on wordpress.org.** Cannot install via REST API by slug — must download zips from GitHub Releases.
- **The elementor-mcp release zipball has an ugly auto-generated folder name** (`Digitizers-elementor-mcp-<sha>/`). WordPress uses the folder name as the plugin slug. Repack with a clean `elementor-mcp/` folder before installing.
- **Claude Code only loads `.mcp.json` at startup** — after writing one, the user must quit and reopen.
- **The `detect-elementor-version` tool errored with a schema validation bug** in v1.5.0 (`elementor_pro_version` null vs. schema `string`). Fixed in current builds and useful for the classic-vs-atomic check — but for the plain auth-works smoke test, `list-pages` is still the simplest.
- **Atomic (V4) tools missing on a V4 site?** Older MCP builds gate atomic-tool registration on `ELEMENTOR_VERSION >= 4.0.0`, but Elementor runs atomic as an experiment while the constant still reads `3.x` — so the tools never register and classic writes silently don't persist. Update the elementor-mcp plugin (the detection now keys off the atomic experiment/module), and on tight tool caps (Antigravity) enable **Low-tools mode** so the 5 atomic essentials stay exposed. See the engine-detection section up top.

## Live-host vs Local differences

**Local-by-Flywheel:** Plugin install via the bundled WP-CLI binary at `/Applications/Local.app/Contents/Resources/extraResources/bin/wp-cli/posix/wp` with PHP at `~/Library/Application Support/Local/lightning-services/php-*/bin/darwin-arm64/bin/php` and the per-site MySQL socket. The setup script automates all of this.

**Live host (cPanel/Cloudways/Kinsta/etc.):** Plugin install via WP Admin → Plugins → Add New → Upload Plugin (manual upload of the two zips). Auth is the same — REST API + Application Password. **MCP URL** changes to `https://<live-domain>/wp-json/mcp/elementor-mcp-server`. **Important:** if the live site is HTTPS (it should be), make sure curl/Claude Code can reach it from your local machine — some hosts block non-browser User-Agents on `/wp-json/`. The setup script's "live" path tests this with a single curl before writing `.mcp.json`.

## Tool-loading discipline

The MCP exposes ~75 deferred tools. Don't load them all at once — fetch schemas lazily as you build:

- **First call:** `list-pages` (no schema needed — pre-loaded by ToolSearch when triggered)
- **Before building containers:** load `get-container-schema`, `add-container`, `update-container`
- **Before placing widgets:** load `add-heading`, `add-text-editor`, `add-button`, `add-image`, `add-html` in one batch
- **Before specific widgets:** load `add-tabs`, `add-icon-list`, `add-divider`, `add-spacer` as needed

Use `ToolSearch` query format `select:tool1,tool2,tool3` to load multiple in one call.

## What the MCP **cannot** do (set expectations)

- Install plugins or themes (use WP-CLI or WP Admin instead) — including **Elementor Pro itself** (paid, not on wp.org; the kit only *detects* it)
- Set the static front page (use `wp option update`)
- Build a custom header/footer on Elementor Free without the HFE plugin *(with Pro, use native Theme Builder via `create-theme-template`)*
- Auto-translate arbitrary HTML/CSS into Elementor widgets — you read the source design and emit widget calls
- Pixel-perfect parity with hand-coded HTML — Elementor's flexbox container model is the ceiling *(Pro adds CSS Grid containers, raising it)*

**Pro features are NOT a limitation when Pro is active** — Form widget, Theme Builder, Loop Grid, Popups, Dynamic Tags, and Sticky/Motion are all driven natively (see the Pro sections above). They're only unavailable on the Free tier, where the documented workarounds apply.

## Optional companion tooling — `wordpress-api-pro` (content/SEO/commerce ops)

> **These are separate, opt-in tools — not a capability of this skill.** This skill drives the Elementor MCP only. The companion toolkit below is a *different* project with its **own credentials and permissions**, and you should reach for it **only when the user explicitly asks** for one of the content/SEO/media/ACF/WooCommerce tasks it covers. Do not silently invoke it, and do not treat its abilities as automatically available here.

The Elementor MCP is for **building and editing page structure** (containers, widgets, Pro widgets). It does **not** cover bulk content ops, media-library uploads, SEO metadata, custom fields, or WooCommerce. When the user asks for one of those, a sibling toolkit — **[`wordpress-api-pro`](https://github.com/Digitizers/wordpress-api-pro)** (Python REST scripts, App-Password auth) — fills the gaps. It authenticates with **its own environment-based credentials** (`WP_URL` / `WP_USERNAME` / `WP_APP_PASSWORD`), separate from this skill's `.mcp.json`, though it can target the same site.

This skill is one stage of the studio toolbox (audit → build → content → host → ads). **Full handoffs + a "where am I" router → load `references/lifecycle.md`.**

**When the user explicitly asks for one of these, `wordpress-api-pro` is the right tool instead of the MCP:**

| Task | Script |
|---|---|
| Upload an actual image/file to the media library (then feed its URL/ID to an Elementor Image widget) | `upload_media.py` |
| Read/write SEO meta (Rank Math / Yoast) | `seo_meta.py` |
| Read/write ACF or JetEngine custom fields | `acf_fields.py` / `jetengine_fields.py` |
| List/create/update WooCommerce products | `woo_products.py` |
| Bulk content changes across many posts or **multiple sites** (dry-run first) | `batch_update.py`, `wp.sh` |
| Plain post/page CRUD outside Elementor | `create_post.py` / `update_post.py` / `get_post.py` / `list_posts.py` |

**Division of labor:** build the page with the MCP → upload media + set SEO meta + wire custom fields/products with `wordpress-api-pro`. Both touch `_elementor_data`, but prefer the **MCP** for structured Elementor edits and reserve `wordpress-api-pro`'s `elementor_content.py` for scripted/batch field tweaks.

> Setup: the scripts need Python 3.8+ and `requests` (`pip install requests`, or a venv). Auth via `WP_URL` / `WP_USERNAME` / `WP_APP_PASSWORD` env vars, or `config/sites.json` for multi-site. See that repo's `SKILL.md`.

## Quick reference — the build flow that works *(mode 1 only)*

> Use this flow only after the user has explicitly chosen "Build" or asked to build a new site/page. Do **not** run this flow as a default response to `/siteagent-elementor-studio` — see the First Action Protocol at the top.

```
1. setup-elementor-mcp.sh          # one-time, ~3 minutes
2. Quit + reopen Claude Code       # picks up .mcp.json
3. list-pages                      # confirm auth
4. get-global-settings             # see current kit
5. update-global-colors + typography
6. create-page (Elementor Canvas template)
7. Set as front page via WP-CLI
8. Build sections top-down, one at a time
9. After each: get-page-structure or curl the front page
10. Pause for human review before header/footer
```

When working from a designed HTML mockup, map the source design to Elementor like this:

- **Brand colors** → `update-global-colors`
- **Brand fonts** → `update-global-typography`
- **Section copy** → `add-heading` + `add-text-editor` widgets
- **Card grids (4+ identical items)** → build one card with native widgets, then `duplicate-element` and `update-element` per copy
- **Tabs/accordions** → native `add-tabs`/`add-accordion` widgets *(HTML allowed inside `tab_content` strings only — see anti-pattern section)*
- **Forms** → real Fluent Forms shortcode via `add-shortcode` widget *(see Fluent Forms section)*
- **Headers/footers** → `elementor-hf` post type with UAE Nav Menu widget for nav

> 🚨 **Final reminder:** Default to native widgets. The HTML widget is only for the four narrow cases listed in the anti-pattern section. Never paste a complete page section as raw HTML — the user must be able to edit the result inside Elementor.
