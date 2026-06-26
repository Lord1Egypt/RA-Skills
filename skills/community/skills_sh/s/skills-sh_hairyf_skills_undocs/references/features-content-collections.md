---
name: undocs-content-collections
description: Content collections configuration and include/exclude patterns in undocs
---

# Content Collections

Undocs uses Nuxt Content collections for documentation. Content is configured in `content.config.ts` within the undocs app layer.

## Default Collection

```typescript
content: defineCollection({
  type: "page",
  source: {
    cwd: globalThis.__DOCS_CWD__,
    include: "**/*.{md,yml}",
    exclude: ["**/.**/**", "**/node_modules/**", "**/dist/**", "**/.docs/**"],
  },
})
```

### Source

- **cwd**: Set to `__DOCS_CWD__` (docs directory from CLI)
- **include**: All markdown and YAML files recursively
- **exclude**: Hidden dirs, node_modules, dist, .docs

## Include Patterns

```
**/*.{md,yml}
```

- `**` — Any directory depth
- `*.md` — Markdown files
- `*.yml` — YAML files (e.g., .navigation.yml)

## Exclude Patterns

| Pattern | Purpose |
|---------|---------|
| `**/.**/**` | Files inside hidden directories (except .config, .partials which may be included via automd) |
| `**/node_modules/**` | Dependencies |
| `**/dist/**` | Build output |
| `**/.docs/**` | Internal .docs directory (public assets, etc.) |

### Hidden Directories

- `.config/` — Config files; content may reference but not directly in collection
- `.docs/` — Excluded; contains public assets
- `.partials/` — Partials; included via automd:file, not as pages
- `.foo/` — Example; excluded by `**/.**/**`

## Collection Type

`type: "page"` — Standard page content with Nuxt Content page features (title, description, toc, etc.)

## Customization

The content config is part of the undocs app layer. To customize:

1. Extend undocs and override content config in your docs layer
2. Use `.config/` for docs-specific config that undocs merges

## Key Points

- Single `content` collection for all docs
- Include: `**/*.{md,yml}`
- Exclude: hidden dirs, node_modules, dist, .docs
- cwd is set at runtime from CLI docs directory

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/content.config.ts
- https://content.nuxt.com/docs/get-started/collections
-->
