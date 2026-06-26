# Slidev Layouts

Using built-in layouts and creating custom ones.

## Applying Layouts

Set the layout in per-slide frontmatter.
```markdown
---
layout: center
---

# Centered Content

This slide uses the center layout.
```

The first slide defaults to `cover` if no layout is specified.

## Built-in Layouts
```yaml
layout: default       # Standard slide with content area
layout: cover         # Title/cover slide (default for first slide)
layout: center        # Vertically and horizontally centered
layout: intro         # Introduction slide
layout: section       # Section divider
layout: statement     # Statement emphasis
layout: quote         # Quote display
layout: fact          # Fact/statistic display
layout: full          # Full page, no padding
layout: end           # Ending slide
layout: none          # No layout wrapper
layout: image         # Full background image
layout: image-left    # Image left, content right
layout: image-right   # Image right, content left
layout: iframe        # Full iframe embed
layout: iframe-left   # Iframe left, content right
layout: iframe-right  # Iframe right, content left
layout: two-cols      # Two columns
layout: two-cols-header # Two columns with header
```

## Two-Column Layout

Use `::right::` to separate left and right content.
```markdown
---
layout: two-cols
---

# Left Side

- Item one
- Item two
- Item three

::right::

# Right Side

- Item A
- Item B
- Item C
```

Without `::right::`, all content goes to the left column.

## Two-Columns with Header

Use `::left::` and `::right::` slots.
```markdown
---
layout: two-cols-header
---

# Header Spanning Both Columns

::left::

Left column content here.

::right::

Right column content here.
```

## Image Layouts

Provide the image source in frontmatter.
```markdown
---
layout: image
image: /background.jpg
---

---
layout: image-left
image: /photo.png
---

# Content on Right

Text appears on the right side.

---
layout: image-right
image: /diagram.svg
class: text-left
---

# Content on Left

Text appears on the left side.
```

Images MUST be in the `public` folder with absolute paths.

## Iframe Layouts

Embed external content.
```markdown
---
layout: iframe
url: https://example.com
---

---
layout: iframe-right
url: https://github.com
---

# GitHub

Content on the left, iframe on the right.
```

## Named Slots

Layouts can define named slots using Vue's slot syntax.
```markdown
---
layout: two-cols
---

::default::

Content for the default (left) slot.

::right::

Content for the right slot.
```

Slot names are defined by the layout. Check the layout source to see available slots.

## Custom Layouts

Create custom layouts in `layouts/` directory.
```
project/
├── layouts/
│   └── my-layout.vue
└── slides.md
```

`layouts/my-layout.vue`:
```vue
<template>
  <div class="slidev-layout my-layout">
    <div class="header">
      <slot name="header" />
    </div>
    <div class="content">
      <slot />
    </div>
    <div class="footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style scoped>
.my-layout {
  display: grid;
  grid-template-rows: auto 1fr auto;
  height: 100%;
  padding: 2rem;
}
</style>
```

Use in slides:
```markdown
---
layout: my-layout
---

::header::
Custom Header

::default::
Main content here.

::footer::
Footer content
```

## Layout Props

Pass props to layouts via frontmatter.
```markdown
---
layout: image-right
image: /photo.jpg
class: text-center
backgroundSize: contain
---
```

Available props depend on the layout. Common props:

- `class` - CSS classes for the slide
- `image` - Image source for image layouts
- `backgroundSize` - CSS background-size value
- `url` - URL for iframe layouts