# Rendshot MCP Tools Reference

## generate_image

Render HTML/CSS, a template, or AI-generated design to image.

**Modes** (mutually exclusive, except prompt+template_id):
- `html` — raw HTML string
- `template_id` — fill a saved template with variables
- `prompt` — AI generates design from natural language
- `prompt` + `template_id` — AI generates using template as style reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `html` | string | — | HTML to render |
| `template_id` | string | — | Template ID (tpl_xxx) |
| `variables` | object | — | Key-value pairs for template |
| `css` | string | — | Additional CSS |
| `prompt` | string | — | Natural language design prompt |
| `platform` | string | — | Platform preset for AI style |
| `locale` | "zh"\|"en" | "zh" | AI response language |
| `width` | number | 1080 | Width in px |
| `height` | number | 1080 | Height in px |
| `format` | "png"\|"jpg" | "png" | Output format |
| `quality` | number | 90 | JPG quality (1-100) |
| `deviceScale` | 1\|2\|3 | 1 | Retina scale factor |
| `fonts` | string[] | — | Custom fonts to load |
| `timeout` | number | 10000 | Render timeout (ms) |

**Returns**: `{ imageId, url, width, height, format, size, createdAt }` — AI mode also returns `{ html, variables }`.

---

## screenshot_url

Capture a webpage as image.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | (required) | URL to screenshot |
| `width` | number | 1280 | Viewport width |
| `height` | number | 800 | Viewport height |
| `format` | "png"\|"jpg" | "png" | Output format |
| `quality` | number | 90 | JPG quality |
| `fullPage` | boolean | false | Capture entire page |
| `deviceScale` | 1\|2\|3 | 1 | Scale factor |
| `timeout` | number | 10000 | Timeout (ms) |

**Returns**: `{ imageId, url, width, height, format, size, createdAt }`

---

## list_templates

Browse community templates.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `platform` | string | — | Filter by platform |
| `category` | string | — | Filter by category |
| `q` | string | — | Search by name/description |
| `limit` | number | 20 | Results per page (1-50) |
| `cursor` | string | — | Pagination cursor |

**Returns**: List of `{ id, name, width, height, variables: [{ key, type }] }` + `nextCursor`.

---

## get_template

Get full template details including variable schema.

| Parameter | Type | Description |
|-----------|------|-------------|
| `template_id` | string | Template ID (required) |

**Returns**: `{ id, name, description, platform, category, width, height, tags, author, thumbnailUrl, variables, createdAt, publishedAt }`.

Each variable: `{ key, type, label, default, required, maxLength, min, max, options }`.

---

## create_template

Save a template for reuse. Created as private draft.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | string | (required) | Template name |
| `html` | string | (required) | HTML with `{{variable}}` placeholders |
| `variables` | array | (required) | Variable definitions |
| `description` | string | — | Description |
| `platform` | string | — | Platform preset |
| `category` | string | — | Category |
| `tags` | string[] | — | Discovery tags |
| `width` | number | — | Width |
| `height` | number | — | Height |
| `css` | string | — | CSS styles |
| `fonts` | string[] | — | Custom fonts |
| `visibility` | "public"\|"private" | "private" | Visibility |

Variable definition shape:
```json
{
  "key": "title",
  "type": "text",
  "label": "Title",
  "default": "Hello",
  "required": true,
  "maxLength": 50
}
```

**Returns**: `{ id, name, status, visibility, width, height }`
