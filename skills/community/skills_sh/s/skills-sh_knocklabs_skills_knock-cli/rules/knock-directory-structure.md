---
title: Knock directory structure
description: Understanding the knock directory layout, configuration files, and resource organization
tags:
  - knock
  - cli
  - directory-structure
  - configuration
  - knock-json
  - workflows
  - layouts
category: knock-cli
last_updated: 2026-02-16
---

# Knock directory structure

## Project configuration

### The knock.json file

Running `knock init` creates a `knock.json` file in your project root. This file configures where Knock resources are stored.

**Basic structure:**

```json
{
  "knockDir": "./knock"
}
```

**Configuration options:**

| Property | Description | Default |
|----------|-------------|---------|
| `knockDir` | Path to the directory containing Knock resources | `./knock` |

The `knockDir` is relative to the location of `knock.json`. All CLI operations use this directory as the root for reading and writing resources.

## Directory layout

The knock directory contains subdirectories for each resource type:

```
knock/
├── workflows/                    # Workflow definitions
│   ├── workflow.schema.json      # JSON Schema for validation
│   └── {workflow-key}/           # One directory per workflow
│       ├── workflow.json         # Main workflow definition
│       └── {step-ref}/           # Channel step content (optional)
│           └── ...               # Template files
│
├── email-layouts/                # Email layout templates
│   └── {layout-key}/
│       ├── layout.json           # Layout configuration
│       └── ...                   # Layout template files
│
├── guides/                       # In-app guides (lifecycle messaging)
│   └── {guide-key}/
│       └── guide.json            # Guide definition and content
│
├── message-types/                # Message type schemas for guides
│   └── {message-type-key}/
│       ├── message_type.json     # Schema and metadata
│       └── preview.html          # Optional; Liquid template for dashboard preview
│
├── translations/                 # Translation files
│   └── {locale}/
│       └── ...                   # Translation JSON files
│
├── partials/                     # Reusable template partials
│   └── {partial-key}/
│       └── ...                   # Partial template files
│
└── commits/                      # Commit history (managed by CLI)
```

## Workflow structure

Each workflow lives in its own directory under `workflows/`:

```
workflows/{workflow-key}/
├── workflow.json                 # Main workflow definition
└── {step-ref}/                   # Directory per channel step (optional)
    └── ...                       # Template content files
```

### workflow.json

The main workflow definition file contains:

```json
{
  "name": "Order Confirmation",
  "description": "Sends order confirmation notifications",
  "categories": ["transactional", "orders"],
  "steps": [
    {
      "ref": "email-step",
      "type": "email",
      "template": {
        "subject": "Order #{{data.order_id}} confirmed",
        "visual_blocks@": "email-step/visual_blocks.json"
      }
    }
  ]
}
```

**Key fields:**

| Field | Description |
|-------|-------------|
| `name` | Display name for the workflow |
| `description` | Optional description |
| `categories` | Optional array of category tags |
| `steps` | Array of workflow steps |

### Step directories

Channel steps (email, SMS, push, etc.) can have their template content extracted into separate files within a step directory:

```
workflows/order-confirmation/
├── workflow.json
└── email-step/
    ├── visual_blocks.json        # Email visual blocks structure
    └── visual_blocks/
        ├── 1.content.md          # First block content
        ├── 2.content.md          # Second block content
        └── ...
```

**When step directories exist:**
- Channel steps with extracted template content
- Complex templates that benefit from separate files

**When step directories don't exist:**
- Function steps (delay, batch, branch, fetch, etc.) never have directories
- Simple templates with inline content

## Email layouts

Email layouts define reusable structure for email templates:

```
email-layouts/{layout-key}/
├── layout.json                   # Layout configuration
├── html_layout.html              # HTML layout template (optional)
└── ...                           # Additional layout files
```

### layout.json

```json
{
  "name": "Default Layout",
  "html_layout@": "html_layout.html",
  "text_layout": "{{ content }}",
  "footer_links": [
    {
      "label": "Unsubscribe",
      "url": "{{ unsubscribe_url }}"
    }
  ]
}
```

## Guides

Guides are in-app UI components for lifecycle messaging (banners, modals, announcements). Each guide lives in its own directory:

```
guides/{guide-key}/
└── guide.json                    # Guide definition with steps and content
```

### guide.json

A guide contains a `name` and a `steps` array. Each step references a message type via `schema_key` and `schema_variant_key`, with content in `values`. See the guides and message types rule file for full details.

## Message types

Message types define the schema for guide content. They live under `message-types/`:

```
message-types/{message-type-key}/
├── message_type.json             # Schema with variants and fields
└── preview.html                  # Optional; Liquid template for dashboard preview
```

### message_type.json

The message type schema defines `name`, `description`, `icon_name`, and `variants`. Each variant has `key`, `name`, and `fields`. The `preview@` field references the preview HTML file. See the guides and message types rule file for schema details.

## File path references

Knock uses the `@` suffix convention to indicate file path references:

```json
{
  "content@": "visual_blocks/1.content.md",
  "html_body@": "body.html",
  "visual_blocks@": "email-step/visual_blocks.json"
}
```

**Path resolution rules:**

1. Paths are **relative to the file containing the reference**
2. In `workflow.json` (at workflow root): paths start from the workflow directory
3. In `visual_blocks.json` (inside step directory): paths are relative to that step directory

**Example:**

```
workflows/my-workflow/
├── workflow.json                 # Uses: "visual_blocks@": "email-step/visual_blocks.json"
└── email-step/
    ├── visual_blocks.json        # Uses: "content@": "visual_blocks/1.content.md"
    └── visual_blocks/
        └── 1.content.md
```

**Common mistake:** Doubling the step directory path. If you're in `email-step/visual_blocks.json`, use `visual_blocks/1.content.md`, NOT `email-step/visual_blocks/1.content.md`.

## JSON Schema

The `workflows/workflow.schema.json` file provides validation for workflow definitions. Reference this schema when:

- Creating or modifying templates
- Working with specific channel types
- Encountering validation errors
- Adding function steps

## Resource identification

Resources are identified by their directory name (the key):

| Resource Type | Key Location | Example |
|---------------|--------------|---------|
| Workflow | Directory name under `workflows/` | `workflows/order-confirmation/` → key: `order-confirmation` |
| Email Layout | Directory name under `email-layouts/` | `email-layouts/default/` → key: `default` |
| Guide | Directory name under `guides/` | `guides/welcome-modal/` → key: `welcome-modal` |
| Message Type | Directory name under `message-types/` | `message-types/banner/` → key: `banner` |
| Partial | Directory name under `partials/` | `partials/footer/` → key: `footer` |

This key is used in CLI commands:

```bash
knock workflow push order-confirmation
knock email-layout push default
knock guide push welcome-modal
knock message-type push banner
```
