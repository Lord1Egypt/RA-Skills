# Webstudio Builder UI

How to work inside the actual Builder app (for when a user asks how to do
something in the UI). Source: official docs (Anatomy of the Webstudio builder,
Modes, Command & search, shortcuts).

## Modes

The Builder has three modes (top bar), plus Safe Mode:

- **Design** - full builder power: add and style components.
- **Content** - editor-only mode for team members/clients. Can edit text/images
  inside Content Blocks, insert templates, create pages from page templates, edit
  safe page settings, and publish (if permitted). Structural/dev settings are
  read-only here.
- **Preview** - hides editing, browse the site, test navigation/interactions/
  responsive behavior on every breakpoint.
- **Safe Mode** - disables all script execution (HTML embeds, custom/third-party
  scripts). Used for security/troubleshooting or reviewing untrusted templates.
  Open from the dashboard (right-click a project > "Open in safe mode").

To test what clients see, switch via the mode dropdown next to Design.

## Canvas

Visual representation of the site you're building. Add components from the
Components Panel, then arrange and style their instances on the canvas.

## Navigator

Hierarchical overview of all instances on the page (nesting + relationships).
Select any instance by clicking it on the canvas or in the Navigator.

- Double-click an instance to rename it (use semantic names like "Hero Section").
- Bottom half = live CSS preview of the selected instance.
- **Global Root** is the highest level, applies to every page. Use it for global
  styles (font size, line height) and defining CSS variables accessible on every
  instance/page. Changing root font size affects all `rem`-based properties.
  Global Root uses the `:root` CSS selector under the hood.

## Breakpoints

Responsive design. Style changes on one breakpoint cascade to it and all smaller
ones. You can create custom breakpoints with ANY media query condition (not just
width) - including `prefers-color-scheme` (dark mode), `prefers-reduced-motion`,
`orientation`, etc. Don't over-add breakpoints or mix min/max-width.

When you select a breakpoint the canvas sizes to the extreme of that breakpoint on
purpose - style for the edge so design issues are caught.

## Components Panel

List of all available components, grouped (General, Text, Media, Forms, Radix).
Click or drag-and-drop onto the canvas.

## Assets Panel

Where static files are stored (upload, organize, manage). Supports Images (JPEG,
PNG, GIF, WebP, SVG, ICO), Fonts (WOFF, WOFF2, TTF, OTF), Documents (PDF, JSON,
XML), and more. Filter/sort by name/date/size. Asset details show name, description,
dimensions, size, uses. Actions: download (Pro), review & delete (shows usages if in
use), delete unused assets (also in Command Panel).

## Style Panel & Style Sources

The top of the Style Panel holds Style Sources: add/select Tokens or switch to
Local styling. Every instance has a Local source (unique to that instance, not
reusable). Convert Local styles to a Token through the token menu. The currently
styled source shows blue; applied properties' labels turn blue. Hover a label for
where a value comes from. See `design.md` for tokens.

## Commands & Search

Use Command Palette (⌘+K) to quickly run actions (e.g. "duplicate tokens", "delete
unused assets"). Also searchable.

## Keyboard shortcuts

The Builder has shortcuts; check the shortcuts doc (Search/⌘+K). Mode switching
needs sufficient permissions (per share-link type).

## Page-level vs global

- Page Settings: page name, path, title, description, SEO, language, social image,
  custom metadata, dynamic paths, redirects, status codes, document type,
  authentication, page variables.
- Project Settings: site-wide config including **Atomic CSS** (toggle to get
  human-readable class names on export instead of atomic styles).

## Share links & permissions

Share dialog creates links with access levels (Build access for CLI sync; Content
permission for client editing). Content-mode share links can optionally grant
publish permission. Pro tier can create Content share links.
