---
name: undocs-custom-icons
description: Add custom icon collections to undocs documentation
---

# Custom Icons

Undocs supports custom icon collections for your documentation site.

## Built-in Icon Collections

Undocs includes two icon collections by default:

1. **undocs** — Project-specific icons (h3, nitro, unplugin, etc.)
   - Located in `app/assets/icons/`
   - Prefix: `undocs-*` (e.g., `i-undocs-h3`)

2. **Nuxt UI** — All icons from Nuxt UI (Heroicons, Lucide, etc.)

## Custom Icon Collection

Add a custom icon collection by placing SVG files in `.docs/icons/`:

```
docs/
├── .config/
│   └── docs.yaml
└── .docs/
    ├── public/
    └── icons/           # Custom icon directory
        ├── my-icon.svg
        └── logo.svg
```

### Icon Format

- Place `.svg` files in the icons directory
- Filename becomes the icon name (without extension)
- Use prefix `custom-*` in markdown or components

### Usage

```markdown
<!-- In markdown -->
:icon{name="i-custom-my-icon"}
```

```vue
<template>
  <UIcon name="i-custom-logo" />
</template>
```

### Navigation Icons

Use custom icons in navigation:

```yaml
# .navigation.yml
icon: i-custom-my-icon
```

Or in frontmatter:

```markdown
---
navigation:
  icon: i-custom-logo
---
```

## Icon Resolution Order

Icons are resolved in this order:

1. `meta.icon` in frontmatter
2. `navigation.icon` in frontmatter or `.navigation.yml`
3. `body.icon` in frontmatter
4. Automatic inference from path (see core-navigation)

## Automatic Icon Inference

When no icon is specified, undocs infers from path using these patterns:

| Path contains | Icon |
|---------------|------|
| guide | `i-lucide-book-open` |
| components | `i-lucide-component` |
| config, configuration | `i-lucide-settings` |
| examples | `i-lucide-code` |
| utils | `i-lucide-square-function` |
| blog | `i-lucide-file-text` |

Inference applies to paths up to 2 directory levels deep.

## Key Points

- Custom icons go in `.docs/icons/` with prefix `custom-*`
- Built-in undocs icons use prefix `undocs-*`
- Icons can be set via frontmatter, `.navigation.yml`, or path inference
- SVG format required for custom icons

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/cli/setup.mjs
- https://github.com/unjs/undocs/blob/main/app/modules/content/icons.ts
- https://github.com/unjs/undocs/blob/main/app/modules/content/hooks.ts
-->
