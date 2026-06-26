---
title: Partials
description: Reusable template building blocks for email design systems and the visual block editor
tags:
  - knock
  - cli
  - partials
  - email
  - design-system
  - visual-blocks
  - templates
category: knock-cli
last_updated: 2026-02-16
---

# Partials

## What partials are

**Partials** are reusable template snippets that can be inserted into email templates via the visual block editor. They serve as building blocks for an email design system—callout cards, quote blocks, comment cards, footers, headers, and other repeatable components.

Partials are:

- Stored in `knock/partials/{key}/`
- Rendered with Liquid; they receive variables from the block editor or from the workflow context
- Available in the email visual block editor when `visual_block_enabled` is true
- Defined by a `partial.json` schema and a content file (HTML, markdown, text, or JSON)

## File structure

Partials live under `knock/partials/{key}/`:

```
partials/{partial-key}/
├── partial.json      # Schema, metadata, and input_schema
└── content.html      # Or content.md, content.txt, content.json
```

The partial key is the directory name and is used in CLI commands: `knock partial push callout-card`.

## partial.json schema

```json
{
  "name": "Callout card",
  "description": "A highlighted callout box for tips and important information.",
  "type": "html",
  "visual_block_enabled": true,
  "content@": "content.html",
  "icon_name": "BellDot",
  "input_schema": [
    {
      "type": "text",
      "key": "title",
      "label": "Title",
      "settings": { "required": false }
    },
    {
      "type": "markdown",
      "key": "body",
      "label": "Body",
      "settings": { "required": true }
    }
  ]
}
```

**Key fields:**

| Field | Description |
|-------|-------------|
| `name` | Display name in the dashboard and block editor |
| `description` | Optional description (max 280 characters) |
| `type` | Content type: `html`, `json`, `markdown`, or `text` |
| `visual_block_enabled` | When true, the partial appears in the email visual block editor |
| `content@` | File path to the content template (relative to the partial directory) |
| `icon_name` | Icon shown in the block editor (e.g., BellDot, Flag) |
| `input_schema` | Array of field definitions for the block editor; same format as a message type variant's `fields` |

## input_schema

The `input_schema` defines the fields that editors see when adding or editing a partial block in the email visual block editor. It uses the **exact same field format** as a message type variant's `fields` array.

Each field has:

- `type` — One of the supported field types
- `key` — Variable name passed to the Liquid template (must match `{{ key }}` in content)
- `label` — Display label in the editor
- `settings` — Object with `required`, `default`, `description`, and type-specific options

### Supported field types

| Type | Description | Settings |
|------|-------------|----------|
| `text` | Single-line text | `required`, `default`, `description`, `min_length`, `max_length` |
| `textarea` | Multi-line plain text | `required`, `default`, `description`, `min_length`, `max_length` |
| `markdown` | Markdown editor (rendered as HTML) | `required`, `default`, `description` |
| `boolean` | Checkbox (true/false) | `required`, `default`, `description` |
| `select` | Single-select from options | `required`, `default`, `description`, `options` (array of `{ label, value }`) |
| `multi_select` | Multi-select from options | `required`, `default`, `description`, `options` |
| `url` | URL field | `required`, `default`, `description` |
| `button` | Button with `text` and `action` subfields | `required`, `text`, `action` (each with `key`, `label`, `settings`) |
| `image` | Image with `url`, `alt`, `action` subfields | `required`, `url`, `alt`, `action` |

### input_schema example

```json
{
  "input_schema": [
    {
      "type": "text",
      "key": "title",
      "label": "Title",
      "settings": {
        "required": false,
        "description": "Optional heading"
      }
    },
    {
      "type": "markdown",
      "key": "body",
      "label": "Body",
      "settings": {
        "required": true,
        "description": "The main content"
      }
    },
    {
      "type": "select",
      "key": "type",
      "label": "Type",
      "settings": {
        "required": false,
        "default": "info",
        "options": [
          { "label": "Info", "value": "info" },
          { "label": "Warning", "value": "warning" }
        ]
      }
    }
  ]
}
```

The field `key` values become Liquid variables in the content template: `{{ title }}`, `{{ body }}`, `{{ type }}`.

## Partial types

| Type | Content file | Use case |
|------|--------------|----------|
| `html` | `content.html` | Email design system components (callouts, cards, blocks) |
| `markdown` | `content.md` | Markdown snippets |
| `text` | `content.txt` | Plain text snippets |
| `json` | `content.json` | Structured data blocks |

For email design systems, `html` is the most common type. Use inline styles for email client compatibility.

## CLI commands

### List partials

```bash
knock partial list
```

### Create a new partial

```bash
# Interactive; use flags to skip prompts
knock partial new -k <partial-key> -n "Partial name" -t html --force
```

| Flag | Description |
|------|-------------|
| `-k`, `--key` | The partial key (directory name) |
| `-n`, `--name` | Display name |
| `-t`, `--type` | `html`, `json`, `markdown`, or `text` |
| `--force` | Skip confirmation prompts |
| `-p`, `--push` | Push to Knock after creation |

### Pull partials

```bash
# Pull all partials
knock partial pull --all --force

# Pull a specific partial
knock partial pull <partial-key> --force
```

Use `--force` to skip "Create a new partial directory?" prompts when the directory does not exist locally.

### Push partials

```bash
# Push all partials
knock partial push --all

# Push a specific partial
knock partial push <partial-key>
```

### Validate partials

```bash
knock partial validate <partial-key>
knock partial validate --all
```

### Other commands

```bash
knock partial get <partial-key>    # Display a single partial
knock partial open <partial-key>   # Open in Knock dashboard
```

## Creating a partial end-to-end

1. **Create the partial locally**

   ```bash
   knock partial new -k callout-card -n "Callout card" -t html --force
   ```

2. **Edit partial.json** — Add `description`, `visual_block_enabled`, and `input_schema` with fields matching the variables your content template expects.

3. **Edit the content file** — Write the Liquid template (e.g., `content.html`) using `{{ key }}` for each input_schema field.

4. **Validate**

   ```bash
   knock partial validate callout-card
   ```

5. **Push**

   ```bash
   knock partial push callout-card
   ```

6. **Commit** (optional) — Use `knock commit -m "Add callout-card partial" --force` to commit the change in Knock.

## Using partials in templates

When a partial is added as a visual block in an email template, Knock renders it with the values editors provide in the block editor. Those values come from the `input_schema` fields and are passed as Liquid variables.

In your partial content, reference them by key:

```liquid
<table>
  <tr>
    <td>{{ body }}</td>
  </tr>
</table>
```

Partials can also use workflow context: `data`, `vars`, `recipient`, `actor`, `tenant`. Use `data.` for trigger payload values, not `vars.`.

## Key gotchas

### Push after every change

Local edits to partials are not synced to Knock until you push. Run `knock partial push <key>` after modifying any partial file.

### Use --force on pulls

When pulling a partial that does not exist locally, the CLI prompts for confirmation. Pass `--force` to skip the prompt in automated contexts.

### visual_block_enabled required for email editor

Only partials with `visual_block_enabled: true` appear in the email visual block editor. HTML partials without this flag are not available as blocks.

### input_schema keys must match content variables

Each `input_schema` field's `key` must correspond to a variable used in the content template. A field with `key: "author_name"` should be referenced as `{{ author_name }}` in the content.

### Path resolution for content@

The `content@` path is relative to the partial directory. Use `"content@": "content.html"` for a file in the same directory.

## Best practices

1. **Design system thinking** — Build partials as reusable components (callouts, quotes, cards, dividers) that enforce consistent styling across emails.

2. **Keep partials focused** — One partial, one purpose. Avoid monolithic partials that try to handle many use cases.

3. **Use input_schema** — Always define `input_schema` for partials used in the visual block editor so editors get proper form fields instead of raw Liquid.

4. **Email-safe HTML** — Use inline styles and table-based layouts for HTML partials. Avoid external CSS, flexbox, or grid for broad email client support.

5. **Provide defaults** — Use Liquid defaults for optional values: `{{ title | default: "Untitled" }}`.

6. **Discover before creating** — Run `knock partial list` to see existing partials and avoid key collisions.
