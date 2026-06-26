---
name: undocs-writing-best-practices
description: Best practices for writing documentation content in undocs
---

# Writing Best Practices

Best practices for structuring and writing documentation content in undocs.

## Page Structure

### Title and Description

Undocs derives page metadata from the first elements:

1. **Title**: First `# h1` is used as page title and removed from body
2. **Description**: First blockquote (that doesn't start with `!`) is used as page description and removed from body

```markdown
# Getting Started

> A brief overview that appears in meta tags and search results.

Your actual content starts here...
```

**Important**: Blockquotes starting with `!` (e.g., `> [!NOTE]`) are GitHub alerts and are NOT used as descriptions — they remain in the body and render as alert components.

### Index Pages

Use numbered prefixes for ordering:

```
1.guide/
  1.index.md      # /guide
2.config/
  1.index.md      # /config
```

The `1.index.md` pattern ensures the index appears first in navigation.

## Reusable Content with Partials

Use the `.partials/` directory for reusable snippets and automd for inclusion:

```
docs/
├── .partials/
│   └── warn.md       # Shared warning block
└── 1.guide/
    └── 1.index.md
```

```markdown
<!-- automd:file src="../.partials/warn.md" -->

> [!IMPORTANT]
> This feature is experimental.

<!-- /automd -->
```

Benefits:

- Single source of truth for repeated content
- automd transforms run before parse, so partials are inlined
- Useful for disclaimers, notes, or legal text

## Leading Blockquote Pattern

For pages that need a visible intro without using it as meta description:

```markdown
# Page Title

> [!NOTE]
> This note stays in the body as an alert.

Rest of content...
```

For pages where the first blockquote should be the meta description:

```markdown
# API Reference

> Complete API documentation for the package.

Actual content...
```

## Code Examples

### Named Code Blocks

Use named code blocks for automatic grouping:

````markdown
```json [package.json]
{ "scripts": { "dev": "undocs dev" } }
```

```ts [config.ts]
export default defineConfig({})
```
````

### Package Manager Commands

Use package manager components for cross-pm compatibility:

```mdc
:pm-install{name="undocs"}
:pm-run{script="dev"}
:pm-x{command="giget gh:unjs/undocs/template docs"}
```

## Steps

Numbered lists with content become step components:

```markdown
1. First step

   :pm-install{name="package"}

2. Second step

   :pm-run{script="dev"}

3. Done ✅
```

**Requirements**: At least one list item must have content; list cannot be nested in another component; content needs at least 2 tabs indentation.

## Key Points

- First h1 = title, first non-alert blockquote = description
- Use `.partials/` and automd:file for reusable content
- Blockquotes starting with `!` are alerts, not descriptions
- Numbered prefixes control navigation order
- Named code blocks auto-group; use pm-* components for commands

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/modules/content/hooks.ts
- https://undocs.unjs.io/guide/components/content-transformation
-->
