# Header / Footer — reference

## Header/Footer notes

Branch on the Pro detection from the top of this skill.

### If Pro → native Theme Builder (preferred)

With Elementor Pro active, build headers/footers/single/archive templates with the
native **Theme Builder** via the `create-theme-template` MCP tool — no UAE/HFE
plugin needed.

1. **Create the template.** `create-theme-template` with the template type:
   - `header`, `footer`, `single` (single post/page), `archive` (post listings).
   The tool returns a `post_id` you build into like any page.
2. **Build the layout** into that `post_id` with native widgets — a row Container
   with logo (Site Logo widget) + native **Nav Menu** widget (`add-nav-menu`,
   Pro) pointed at a WP menu by name + a Button CTA.
3. **Set display conditions** so the template applies site-wide (or to a subset).
   Theme Builder display conditions are Pro-native; configure "Entire Site" for a
   global header/footer.
4. **Verify** by curling the front page — the header/footer should render on every
   matching page.

> The WordPress **menu itself** still must exist first (WP Admin → Appearance →
> Menus) — the MCP cannot create WP nav menus directly, on either tier. Point the
> Nav Menu widget at it by name.

### If Free → UAE / HFE workaround (fallback)

`create-theme-template` is **not exposed** without Pro. With Elementor Free, headers and footers are built using **Ultimate Addons for Elementor (UAE)** by Brainstorm Force (the kit's setup wizard auto-installs this; alternatively the lighter **Header Footer Elementor (HFE)** plugin from the same company also works — both share the same `elementor-hf` post type).

### Building a site-wide header

1. **Create the WordPress menu first.** Tell the user to go to WP Admin → Appearance → Menus, name it (e.g. "Main"), add the pages they want, and save. The MCP cannot create WP nav menus directly — this step is a one-minute manual action.

2. **Create the header template post.** Use `create-page` with `post_type: "elementor-hf"` and a title like "Site Header". Then set the following post meta via WP-CLI or the `update-element` flow:
   - `ehf_template_type` = `"type_header"` (or `"type_footer"` for footers)
   - `display-on-canvas` = `"yes"` (displays site-wide; alternative meta keys like `ehf_target_include_locations` may apply for narrower scopes)

3. **Build the layout.** A row container with three children:
   - **Left:** logo (Heading widget with brand name in display serif, OR `Site Logo` widget if UAE is installed)
   - **Center:** **UAE Nav Menu widget** (`uael-nav-menu`) pointed at the WordPress menu by name. UAE's nav menu widget is **free** and handles mobile hamburger, dropdowns, hover states, active-page highlighting automatically — much cleaner than rendering nav as raw HTML.
   - **Right:** Button widget with "Contact" or "Get In Touch" CTA

4. **Verify display.** After building, instruct the user to check WP Admin → Appearance → Header Footer Builder → confirm the Display On rule is set to "Entire Website."

### When UAE Nav Menu isn't available

If only HFE (the lighter plugin) is installed without UAE: use the Shortcode widget calling `[wp_nav_menu menu="Main" container=""]` — WordPress's built-in shortcode renders the menu as a real `<ul>` with all the right classes for active-page highlighting and responsive styling.

**Do not** fall back to manually listing the menu items inside an HTML widget — that hard-codes the navigation in two places (the WP menu AND the Elementor template) which means future menu edits won't reflect in the header. Always render the menu through `[wp_nav_menu]` or the UAE widget.

### Footer pattern

Identical post type (`elementor-hf`) but `ehf_template_type = "type_footer"`. Layout is typically a 4-column container (brand block + 3 link columns) on a dark background, with a bottom row containing copyright + social icons.

