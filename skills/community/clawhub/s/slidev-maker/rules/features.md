# Slidev Features

LaTeX math, slide imports, global layers, shortcuts, and other authoring features.

## LaTeX Math

Slidev renders math with KaTeX.

Inline math:
```md
Pythagorean theorem: $a^2 + b^2 = c^2$
```

Block math:
```md
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

## Importing Slides

Split a large deck into multiple files and compose them with `src:` in frontmatter. Each imported file is inserted in place:
```md
---
src: ./slides/intro.md
---

---
src: ./slides/content.md
---
```

The importing slide can still add its own frontmatter; imported files may have their own headmatter-style options applied per slide.

## Global Layers

Persistent UI shown on every slide. Create `global-top.vue` and/or `global-bottom.vue` at project root:
```vue
<!-- global-top.vue -->
<template>
  <div class="fixed top-0 left-0 right-0 p-4">
    Header content on all slides
  </div>
</template>
```

`global-bottom.vue` renders beneath slide content; `global-top.vue` renders above it.

## Custom Keyboard Shortcuts

Remap navigation keys in headmatter:
```yaml
---
shortcuts:
  next: space
  prev: shift+space
  toggleOverview: o
---
```

For the default shortcut table and presenter controls, see `presenter.md`.

## Routes / Named Slides

Give a slide a route alias so `<Link>` can target it by name (see `components.md`):
```yaml
---
routeAlias: solutions
---
```

## Related Features Documented Elsewhere

- **Code blocks** (Shiki, line highlighting, Monaco, Magic Move, TwoSlash) → `code-blocks.md`
- **Diagrams** (Mermaid, PlantUML) → `diagrams.md`
- **Icons** (Iconify, `<carbon-logo-github />`) → `assets.md`
- **Images / video / fonts** → `assets.md`
- **Drawing, recording, remote control, speaker notes** → `presenter.md`
- **Animations & transitions** (v-click, v-motion, v-mark) → `animations.md`
- **Styling & UnoCSS** → `styling.md`
