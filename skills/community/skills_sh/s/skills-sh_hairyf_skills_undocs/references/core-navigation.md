---
name: undocs-navigation
description: Understand how navigation works in undocs and how to customize it
---

# Navigation System

Undocs automatically generates navigation from your documentation structure. Navigation is based on Nuxt Content's file-based routing.

## Automatic Navigation

Navigation is automatically generated from your directory structure:

```
docs/
├── 1.guide/
│   ├── 1.index.md          # /guide
│   └── components/
│       ├── components.md   # /guide/components/components
│       └── content-transformation.md
└── 2.config/
    └── 1.index.md         # /config
```

The numbered prefixes (e.g., `1.guide`, `2.config`) determine the order in navigation.

## Navigation Configuration

### Custom Navigation Icon

Set icons for navigation items using `.navigation.yml` files:

```yaml
# .navigation.yml
icon: i-lucide-book-open
```

Or in frontmatter:

```markdown
---
navigation:
  icon: i-lucide-settings
---
```

### Automatic Icon Inference

Icons are automatically inferred from path names:

- `guide` → `i-lucide-book-open`
- `components` → `i-lucide-component`
- `config` / `configuration` → `i-lucide-settings`
- `examples` → `i-lucide-code`
- `utils` → `i-lucide-square-function`
- `blog` → `i-lucide-file-text`

Icons are resolved from:
1. `meta.icon` in frontmatter
2. `navigation.icon` in frontmatter
3. `body.icon` in frontmatter
4. Automatic inference from path

## Navigation Behavior

### Single Child Flattening

If a navigation item has only one child, it's automatically flattened:

```
Before:
- Guide
  - Getting Started

After:
- Getting Started (directly under Guide)
```

### Index Page Resolution

If a section has children but no index page, navigation automatically resolves to the first child:

```
/guide (no index)
  └── /guide/getting-started (first child)

Navigation shows: /guide/getting-started
```

### Active State

Navigation items are marked as active when the current route starts with their path:

```typescript
const isActive = (path: string) => route.path.startsWith(path);
```

## Breadcrumbs

Breadcrumbs are automatically generated from the navigation structure, showing the hierarchical path to the current page.

## Key Points

- Navigation is file-based and automatic
- Numbered prefixes control order (`1.guide`, `2.config`)
- Icons can be set via `.navigation.yml` or frontmatter
- Single-child items are automatically flattened
- Index pages are resolved to first child if missing
- Breadcrumbs are generated automatically

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/composables/useDocsNav.ts
- https://github.com/unjs/undocs/blob/main/app/modules/content/hooks.ts
-->
