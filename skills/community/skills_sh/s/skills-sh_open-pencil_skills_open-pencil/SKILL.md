---
name: open-pencil
description: Work with Figma .fig design files and the running OpenPencil editor — inspect structure, query nodes, analyze design tokens, export PNG/SVG/PDF/JSX, and modify designs programmatically. Use when asked to open, inspect, export, analyze, or edit .fig files, or to control the running OpenPencil app.
---

# OpenPencil

OpenPencil provides a CLI and MCP server for `.fig` design files and the running OpenPencil editor.

Use two modes:

- **App mode** — connect to the running OpenPencil editor by omitting the file argument.
- **Headless mode** — work with `.fig` files directly by passing a file path.

```bash
# App mode — operates on the document open in the editor
openpencil tree

# Headless mode — operates on a .fig file
openpencil tree design.fig
```

Current reference version: OpenPencil `0.12.x`. The MCP server exposes 106 tools in `0.12.0`.

## Requirements

```bash
# CLI
bun add -g @open-pencil/cli

# MCP server used by the desktop app and external MCP clients
bun add -g @open-pencil/mcp
```

The desktop app starts `openpencil-mcp-http` automatically in production Tauri builds when `@open-pencil/mcp` is installed globally and exposes automation on:

- HTTP/RPC: `http://127.0.0.1:7600`
- WebSocket bridge: `ws://127.0.0.1:7601`
- MCP Streamable HTTP: `http://127.0.0.1:7600/mcp`

## CLI Commands

```bash
openpencil --help
```

Commands in `0.12.x`:

- `info` — document overview: pages, node counts, fonts
- `tree` — print hierarchy with types and sizes
- `pages` — list pages
- `node` — detailed node properties by ID
- `selection` — current selection from the running app
- `find` — find nodes by name/type
- `query` — XPath selectors for node search
- `variables` — list variables and collections
- `export` — export PNG/JPG/WEBP/SVG/PDF/JSX/.fig
- `convert` — convert between supported document formats
- `analyze` — colors, typography, spacing, repeated clusters
- `lint` — consistency, structure, and accessibility checks
- `formats` — supported document/export formats
- `eval` — execute JavaScript with the Figma Plugin API

### Inspect

```bash
openpencil info design.fig
openpencil tree design.fig
openpencil tree --page "Components" --depth 3  # app mode
openpencil pages design.fig
openpencil node design.fig --id 1:23
openpencil node --id 1:23  # app mode
openpencil selection --json
openpencil variables design.fig
openpencil variables --collection "Colors" --type COLOR
```

### Search and XPath query

```bash
openpencil find design.fig --name "Button"
openpencil find --type FRAME                          # app mode
openpencil find design.fig --type TEXT --page "Home"
openpencil find design.fig --name "Card" --type COMPONENT --limit 50

openpencil query design.fig "//FRAME"
openpencil query design.fig "//FRAME[@width < 300]"
openpencil query design.fig "//TEXT[contains(@name, 'Button')]"
openpencil query design.fig "//COMPONENT[@stackMode]"
openpencil query design.fig "//COMPONENT//FRAME//TEXT"
openpencil query "//FRAME[@width > 1000]"             # app mode
```

Common node types: `FRAME`, `TEXT`, `RECTANGLE`, `ELLIPSE`, `VECTOR`, `GROUP`, `COMPONENT`, `COMPONENT_SET`, `INSTANCE`, `SECTION`, `LINE`, `STAR`, `POLYGON`, `SLICE`, `BOOLEAN_OPERATION`.

### Export and convert

```bash
openpencil export design.fig -o hero.png
openpencil export -o hero.png                         # app mode
openpencil export design.fig --node 1:23 -s 2 -o button@2x.png
openpencil export design.fig -f jpg -q 85 -o preview.jpg
openpencil export design.fig -f svg --node 1:23 -o icon.svg
openpencil export design.fig -f pdf -o page.pdf
openpencil export design.fig -f fig -o roundtrip.fig
openpencil export design.fig -f jsx -o component.jsx
openpencil export design.fig -f jsx --style tailwind -o component.tsx
openpencil export design.fig --thumbnail --width 1920 --height 1080
openpencil export --page "Components" -o components.png

openpencil convert design.fig -o design.pen
openpencil formats
```

### Analyze and lint

```bash
openpencil analyze colors design.fig
openpencil analyze colors --similar --threshold 10     # app mode
openpencil analyze typography design.fig --group-by size
openpencil analyze spacing design.fig --grid 8
openpencil analyze clusters design.fig --min-count 3
openpencil lint design.fig
openpencil lint design.fig --json
```

### Eval (Figma Plugin API)

Execute JavaScript against the document using a Figma Plugin API-compatible runtime:

```bash
openpencil eval design.fig -c 'figma.currentPage.findAll(n => n.type === "TEXT").length'

# App mode — modifies the live document in the editor
openpencil eval -c '
  const buttons = figma.currentPage.findAll(n => n.name === "Button");
  buttons.forEach(b => { b.cornerRadius = 8 });
  buttons.length + " buttons updated"
'

# Modify and save to the same file
openpencil eval design.fig -w -c '
  const texts = figma.currentPage.findAll(n => n.type === "TEXT");
  texts.forEach(t => { t.fontSize = 16 });
'

# Save to a different file
openpencil eval design.fig -o modified.fig -c '...'

# Read code from stdin
echo 'figma.currentPage.children.map(n => n.name)' | openpencil eval design.fig --stdin
```

Every command that reports structured data supports `--json` when appropriate.

## MCP Server

### Stdio MCP clients

Use Bun by default:

```json
{
  "mcpServers": {
    "open-pencil": {
      "command": "bunx",
      "args": ["openpencil-mcp"]
    }
  }
}
```

If `@open-pencil/mcp` is installed globally, direct binaries also work:

```json
{
  "mcpServers": {
    "open-pencil": {
      "command": "openpencil-mcp"
    }
  }
}
```

### HTTP / Streamable HTTP

```bash
export PORT=7600
export OPENPENCIL_MCP_AUTH_TOKEN=secret       # optional auth for /mcp
export OPENPENCIL_MCP_CORS_ORIGIN="*"         # optional CORS
export OPENPENCIL_MCP_ROOT=/path/to/files     # enables/scopes open_file/save_file paths

openpencil-mcp-http
# or: bunx openpencil-mcp-http
```

### MCP workflow

1. **Open/create a document** — `open_file { path }` when `OPENPENCIL_MCP_ROOT` is configured, or `new_document {}`.
2. **Query** — `get_page_tree`, `find_nodes`, `query_nodes`, `get_node`, `list_pages`, `get_current_page`.
3. **Inspect** — `get_jsx`, `diff_jsx`, `describe`, `export_image`, `export_svg`, `export_pdf`.
4. **Modify** — `render`, `batch_update`, `update_node`, `set_fill`, `set_layout`, `create_shape`, `import_svg`, etc.
5. **Navigate** — after creating or editing visible canvas content, call `select_nodes` and `viewport_zoom_to_fit { id }` (or `node_bounds` + `viewport_set`) so the user can see the result in the running editor.
6. **Save/export** — `save_file`, `export_image`, `export_svg`, `export_pdf`, or CLI `export`.

## MCP Tools in 0.12.0 (106 total)

**Read and selection (17):** `get_selection`, `get_node`, `find_nodes`, `get_page_tree`, `get_current_page`, `list_pages`, `select_nodes`, `query_nodes`, `get_components`, `switch_page`, `page_bounds`, `list_fonts`, `list_available_fonts`, `get_jsx`, `diff_jsx`, `describe`, `node_tree`

**Create and import (12):** `render`, `create_shape`, `create_component`, `create_instance`, `create_page`, `create_vector`, `create_slice`, `import_svg`, `search_icons`, `insert_icon`, `fetch_icons`, `stock_photo`

**Modify (24):** `update_node`, `batch_update`, `set_layout`, `set_layout_child`, `set_radius`, `set_fill`, `set_stroke`, `set_text`, `set_text_properties`, `set_effects`, `set_opacity`, `set_font`, `set_visible`, `set_constraints`, `set_rotation`, `set_minmax`, `set_font_range`, `set_text_resize`, `set_blend`, `set_locked`, `set_stroke_align`, `set_image_fill`, `set_variable`, `bind_variable`

**Structure (16):** `delete_node`, `reparent_node`, `node_resize`, `clone_node`, `node_move`, `rename_node`, `group_nodes`, `ungroup_node`, `flatten_nodes`, `node_to_component`, `node_bounds`, `node_ancestors`, `node_children`, `node_bindings`, `node_replace_with`, `arrange`

**Variables (9):** `list_variables`, `list_collections`, `get_variable`, `find_variables`, `create_variable`, `delete_variable`, `get_collection`, `create_collection`, `delete_collection`

**Vector and viewport (15):** `boolean_union`, `boolean_subtract`, `boolean_intersect`, `boolean_exclude`, `path_get`, `path_set`, `path_scale`, `path_flip`, `path_move`, `viewport_get`, `viewport_set`, `viewport_zoom_to_fit`, `export_svg`, `export_pdf`, `export_image`

**Analyze and generation (9):** `analyze_colors`, `analyze_typography`, `analyze_spacing`, `analyze_clusters`, `diff_create`, `diff_show`, `design_to_tokens`, `design_to_component_map`, `calc`

**File and prompts (4):** `save_file`, `open_file`, `new_document`, `get_codegen_prompt`

> Tool availability can depend on server mode. `open_file`, `save_file`, and disk-writing export paths require `OPENPENCIL_MCP_ROOT` for path scoping.

## Key tools for agents

- **`query_nodes`** — XPath selectors to find specific nodes without fetching the full tree.
- **`get_jsx`** — inspect any node as JSX in the same format accepted by `render`.
- **`diff_jsx`** — compare two nodes structurally before editing.
- **`describe`** — semantic analysis of role, visual style, layout, and design issues.
- **`batch_update`** — apply multiple node updates efficiently.
- **`export_image` / `export_svg` / `export_pdf`** — visual verification and deliverables.
- **`viewport_zoom_to_fit` / `viewport_set` / `viewport_get`** — keep the live editor focused on the created or edited design.
- **`get_codegen_prompt`** — retrieve OpenPencil's current JSX/codegen guidance.

## JSX Rendering

Use the `render` tool or `eval` to create component trees. If unsure about JSX syntax, call `get_codegen_prompt` first.

```jsx
<Frame name="Card" w={320} h="hug" flex="col" gap={16} p={24} bg="#FFF" rounded={16}>
  <Text size={18} weight="bold" color="#111">Title</Text>
  <Text size={14} color="#666">Description text</Text>
  <Frame flex="row" gap={8}>
    <Frame w={80} h={36} bg="#3B82F6" rounded={8} justify="center" items="center">
      <Text size={14} color="#FFF" weight="600">Action</Text>
    </Frame>
  </Frame>
</Frame>
```

Elements: `Frame`, `Text`, `Rectangle`, `Ellipse`, `Line`, `Star`, `Polygon`, `Group`, `Section`, `Component`, `Instance`.

Text content is the child content of `<Text>`. Use design-JSX props, not Figma API field names:

```jsx
<Text size={48} weight="bold" font="Inter" color="#111">Design faster with AI</Text>
```

Common props:

| Prop | Meaning |
|------|---------|
| `w`, `h` | Width, height (number or `"hug"` / `"fill"`) |
| `flex` | `"row"` or `"col"` |
| `grid`, `columns`, `rows` | CSS Grid, e.g. `columns="1fr 200px 1fr"` |
| `gap`, `rowGap`, `columnGap` | Item spacing |
| `p`, `px`, `py`, `pt`, `pr`, `pb`, `pl` | Padding |
| `justify` | `"start"`, `"center"`, `"end"`, `"between"` |
| `items` | `"start"`, `"center"`, `"end"`, `"stretch"` |
| `grow` | Flex grow factor |
| `bg` | Fill color (hex) |
| `rounded`, `roundedTL/TR/BL/BR` | Corner radius |
| `stroke`, `strokeWidth` | Stroke color and weight |
| `opacity` | 0–1 |
| `rotate` | Degrees |
| `overflow` | `"hidden"` to clip children |
| `shadow` | `"offsetX offsetY blur #color"` |
| `blur` | Layer blur |
| `size`, `weight`, `font`, `color`, `textAlign` | Text properties |
| `colStart`, `rowStart`, `colSpan`, `rowSpan` | Grid child positioning |

## Tips

- Omit the file path to work with the document open in the running OpenPencil editor.
- Start with `info` or `get_page_tree` to understand the document.
- Use `tree --depth 2` or `query_nodes` to avoid overwhelming output on large files.
- Export specific nodes with `--node` for faster visual checks.
- Use `export_image` after changes to verify visual quality.
- After creating a visible design, select it and zoom the editor to it: `select_nodes { ids: [id] }` then `viewport_zoom_to_fit { id }`.
- If zoom-to-fit is unavailable in a client, use `node_bounds` to calculate the center and call `viewport_set { x, y, zoom }`.
- Use `analyze colors --similar` to find near-duplicate colors.
- Use `eval` for Figma Plugin API operations not covered by a dedicated CLI/MCP tool.
- Use `--json` when piping CLI output to scripts.
- In app mode, `eval` and MCP modifications are reflected live in the editor.
