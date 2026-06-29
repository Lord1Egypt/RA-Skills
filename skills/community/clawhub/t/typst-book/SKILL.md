---
name: "typst-book"
description: "Write and typeset richly illustrated books with Typst — text, CeTZ vector art, AI-generated images, and full layout control to PDF."
---

# Typst Book — Write & Typeset Illustrated Books

Create richly illustrated books using [Typst](https://github.com/typst/typst), a modern markup-based typesetting system. Combines prose, vector illustrations (CeTZ), AI-generated images, and full layout control into polished PDF/PNG output.

## Prerequisites

### Install Typst

```bash
# Linux x86_64 musl static binary (works on most systems)
curl -sL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz -o /tmp/typst.tar.xz
mkdir -p /tmp/typst-dl && tar xf /tmp/typst.tar.xz -C /tmp/typst-dl
mkdir -p ~/.local/bin
cp /tmp/typst-dl/typst-x86_64-unknown-linux-musl/typst ~/.local/bin/typst
chmod +x ~/.local/bin/typst
# Ensure ~/.local/bin is in PATH
export PATH="$HOME/.local/bin:$PATH"
typst --version  # should print v0.15.0+
```

### Verify

```bash
typst --version    # v0.13+ minimum, v0.15+ recommended for CeTZ 0.5+
typst fonts        # list available fonts
```

## Workflow

### 1. Plan the Book

Before writing, decide:
- **Genre/format**: Children's book, textbook, novel, technical manual, zine, coffee-table book
- **Page size**: A4 (21×29.7cm), US Letter (8.5×11in), custom (e.g. square 20×20cm for children's books)
- **Illustration style**: CeTZ vector art, AI-generated images, SVG imports, or mixed
- **Color palette**: Define a palette up front for consistency
- **Structure**: Front matter (title, copyright, TOC), chapters, back matter

### 2. Set Up Project Structure

```
book-project/
  main.typ           # Entry point, imports chapters
  book.typ           # Book template/helpers (chapter function, styling)
  chapters/
    ch01.typ
    ch02.typ
    ...
  images/            # AI-generated or external images (PNG, JPEG, SVG)
  illustrations/     # CeTZ illustration modules (optional, for complex reusable art)
  output/            # Generated PDFs and PNGs
```

### 3. Write the Book Template

Create `book.typ` with the reusable styling and helper functions:

```typst
#import "@preview/cetz:0.5.2": canvas, draw

// --- Color palette ---
#let palette = (
  primary: rgb("#2c3e50"),
  accent: rgb("#e74c3c"),
  warm: rgb("#f39c12"),
  cool: rgb("#3498db"),
  muted: rgb("#95a5a6"),
  paper: rgb("#fdfdfd"),
)

// --- Page setup ---
#let book-page(width: 21cm, height: 29.7cm, margin: (x: 2.5cm, y: 2.5cm)) = {
  set page(width: width, height: height, margin: margin)
}

// --- Chapter helper ---
#let chapter(title, subtitle: none) = {
  pagebreak(weak: true)
  v(2cm)
  block(width: 100%, {
    align(center)[
      #text(size: 28pt, weight: "bold", fill: palette.primary)[#title]
    ]
    if subtitle != none {
      v(0.4cm)
      align(center)[#text(size: 14pt, fill: palette.muted)[#subtitle]]
    }
  })
  v(1cm)
}

// --- Figure helper with consistent styling ---
#let illustration(body, caption: none) = {
  if caption != none {
    figure(alignment(center)[#body], caption: caption)
  } else {
    align(center)[#body]
  }
  v(0.8em)
}

// --- Decorative divider ---
#let divider() = {
  v(0.5em)
  align(center)[#text(fill: palette.muted)[◆ ◆ ◆]]
  v(0.5em)
}
```

### 4. Write Chapters

`main.typ`:

```typst
#import "book.typ": *

#show: book-page
#set text(font: "DejaVu Serif", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.8em)

#include "chapters/ch01.typ"
#include "chapters/ch02.typ"
```

`chapters/ch01.typ`:

```typst
#import "../book.typ": *

#chapter[Chapter One: The Beginning]

Once upon a time, in a workshop filled with gears and steam, lived Ada.

#illustration(
  canvas({
    import draw
    draw.circle((0, 0), radius: 2, fill: rgb("#ffd93d"))
    draw.circle((-0.6, 0.4), radius: 0.25, fill: black)
    draw.circle((0.6, 0.4), radius: 0.25, fill: black)
    draw.line((-0.5, -0.6), (0.5, -0.6), stroke: 2pt + black)
  }),
  caption: [Ada's first smile]
)
```

### 5. Illustration Methods

Use the right tool for each illustration:

#### A. CeTZ Vector Art (diagrams, characters, abstract shapes)

```typst
#import "@preview/cetz:0.5.2": canvas, draw

#canvas({
  import draw
  // Trees
  draw.line((0, 0), (0, 3), stroke: 4pt + rgb("#8b4513"))
  draw.circle((0, 4), radius: 1.5, fill: rgb("#2ecc71"))
  // Clouds
  draw.circle((-3, 6), radius: 0.8, fill: rgb("#ecf0f1"))
  draw.circle((-2, 6), radius: 1.0, fill: rgb("#ecf0f1"))
  draw.circle((-1, 6), radius: 0.7, fill: rgb("#ecf0f1"))
})
```

CeTZ uses a coordinate system where (0,0) is bottom-left by default. All coordinates are in CeTZ units (not cm/pt). Key functions:
- `draw.line(from, to, stroke: ..)` — lines
- `draw.circle(center, radius: r, fill: ..)` — circles
- `draw.rect(corner, width: w, height: h, fill: ..)` — rectangles
- `draw.content(point, [text])` — inline text at a point
- `draw.curve(..points)` — smooth curves through points
- `draw.arc(center, start: .., stop: .., radius: r)` — arcs

#### B. AI-Generated Images (photographic, painterly, complex scenes)

Use `image_generate` tool to create illustrations, save to `images/` directory, then embed:

```typst
#figure(
  image("images/forest-scene.png", width: 80%),
  caption: [The enchanted forest at dusk]
)
```

Recommended `image_generate` settings for book illustrations:
- `size: "1024x1024"` for spot illustrations
- `size: "1536x1024"` for full-page landscape scenes
- `size: "1024x1536"` for full-page portrait scenes
- `quality: "high"` for print-quality
- `outputFormat: "png"` for lossless quality

#### C. Native Typst Graphics (simple shapes, color blocks, decorative elements)

```typst
#box(width: 100%, height: 3cm, {
  let colors = (rgb("#e74c3c"), rgb("#e67e22"), rgb("#f1c40f"), rgb("#2ecc71"), rgb("#3498db"), rgb("#9b59b6"))
  for (i, c) in colors.enumerate() {
    place(center + horizon, rect(width: 100%/colors.len(), height: 100%, fill: c))
  }
})
```

#### D. SVG Import (external vector graphics)

```typst
#figure(
  image("illustrations/diagram.svg", width: 75%),
  caption: [System architecture]
)
```

Typst natively supports SVG, PNG, JPEG, and GIF formats.

### 6. Compile

```bash
# Compile to PDF
typst compile main.typ output/book.pdf

# Compile to PNG (one per page)
typst compile --format png --ppi 150 main.typ "output/page-{p}.png"

# Watch mode for iterative editing
typst watch main.typ output/book.pdf
```

Always compile from the project root directory so relative paths resolve correctly:

```bash
cd book-project && typst compile main.typ output/book.pdf
```

### 7. Preview and Verify

After compiling:
1. Convert first few pages to PNG for visual inspection
2. Use the `image` tool to review layout quality
3. Check for: text overflow, image sizing, caption alignment, page breaks
4. Reiterate on content and styling

```bash
typst compile --format png --ppi 150 main.typ "output/preview-{p}.png"
# Then use image tool on preview-1.png, preview-2.png, etc.
```

## Key Typst Syntax Reference

### Markup
- `= Heading`, `== Subheading` — headings (number of = = level)
- `*bold*`, `_italic_` — text styling
- `- item` — bullet list
- `+ item` — numbered list
- `[link](url)` — links
- `` `code` `` — inline code
- `---` — em dash, `~` — non-breaking space

### Page & Layout
- `#set page(width: 21cm, height: 29.7cm, margin: 2cm)` — page setup
- `#set text(font: "DejaVu Serif", size: 12pt)` — typography
- `#set par(justify: true, leading: 0.8em)` — paragraph settings
- `#pagebreak()` — forced page break
- `#v(2cm)` / `#h(1cm)` — vertical/horizontal space
- `#align(center)[content]` — alignment
- `#box[..]`, `#block[..]` — inline/block containers
- `#grid(columns: 2, ..items)` — multi-column layouts
- `#place(center + horizon, ..)` — absolute positioning

### Figures
- `#figure(body, caption: [text])` — numbered figure with caption
- `#figure(image("file.png", width: 80%), caption: [desc])` — image figure
- `#outline(title: [Table of Contents])` — auto-generated TOC

### Scripting
- `#let name = value` — variable binding
- `#let func(x) = { .. }` — function definition
- `#if condition { .. } else { .. }` — conditionals
- `#for item in items { .. }` — iteration
- `#include "file.typ"` — include another file
- `#import "module.typ": func1, func2` — import from module

### Show Rules (styling)
- `#show heading: it => [custom heading]` — restyle elements
- `#show figure.where(kind: image): it => [..]` — restyle specific figures
- `#set heading(numbering: "1.")` — auto-number headings

## CeTZ Quick Reference

```typst
#import "@preview/cetz:0.5.2": canvas, draw

#canvas({
  import draw
  // Shapes
  draw.line((0, 0), (5, 5), stroke: 2pt + red)
  draw.circle((2, 2), radius: 1, fill: blue, stroke: 1pt + dark-blue)
  draw.rect((0, 0), (4, 2), fill: green, stroke: black)
  draw.square((1, 1), size: 2, fill: yellow)
  draw.ellipse((3, 3), rx: 2, ry: 1, fill: purple)
  draw.curve((0, 0), (1, 2), (2, 0), (3, 2), stroke: 1pt)
  draw.arc((2, 2), start: 0deg, stop: 180deg, radius: 2)
  // Text at point
  draw.content((2, 4), [Label], fill: red)
  // Groups
  draw.group(name: "scene", {
    draw.circle((0, 0), radius: 1, fill: blue)
    draw.circle((2, 0), radius: 1, fill: red)
  })
  // Transformations
  draw.rotate(45deg, {
    draw.rect((0, 0), (4, 1), fill: orange)
  })
  draw.scale(2, {
    draw.circle((0, 0), radius: 1, fill: teal)
  })
})
```

## Tips & Gotchas

- **CeTZ coordinates** are in abstract units, not cm/pt. Scale the canvas with `#canvas(length: 1cm, { .. })` to set unit scale.
- **Fonts**: Use `typst fonts` to list available fonts. Common: DejaVu Serif, DejaVu Sans, FreeSerif, Latin Modern Roman, JetBrains Mono.
- **Package downloads**: Typst auto-downloads `@preview/` packages on first compile. Requires network access.
- **Image paths**: Relative to the `.typ` source file, not the output path. Use `--root` for absolute paths.
- **Large images**: PNG files can bloat the PDF. Use JPEG for photographic content when lossless isn't needed.
- **Page numbering**: `#set page(numbering: "1")` for Arabic, `"i"` for Roman, `none` to skip.
- **Front matter**: Use `#set page(numbering: "i")` before main content, then `#set page(numbering: "1")` at chapter 1.
- **Heading numbering**: `#set heading(numbering: "1.1.a")` for "1.1.a" style.
- **Blank pages**: `#pagebreak()` creates a blank page (useful for chapter spacing).
- **Color opacity**: `rgb("#ff000088")` — last two hex digits are alpha.
- **Gradients**: `gradient.linear(rgb("#ff6b6b"), rgb("#4ecdc4"))` for linear gradients.
- **Tiling**: Use `#place(..)` for absolute positioning of decorative elements like corner flourishes.

## Output Delivery

When delivering the final book to the user:
1. Compile to PDF as the primary deliverable
2. Also export PNG previews of key pages
3. Attach the PDF using `MEDIA:<path>` in the reply
4. Clean up temporary files

## Example: Minimal Children's Book

```typst
#import "@preview/cetz:0.5.2": canvas, draw

#set page(width: 20cm, height: 20cm, margin: 2cm)
#set text(font: "DejaVu Serif", size: 14pt)

#align(center)[
  #v(2cm)
  #text(size: 32pt, weight: "bold", fill: rgb("#e74c3c"))[The Tiny Seed]
  #v(1cm)
]

#pagebreak()

In a small garden, a tiny seed slept beneath the soil.

#v(0.5cm)
#align(center)[
  #canvas({
    import draw
    draw.rect((0, 0), (6, 3), fill: rgb("#8b4513"))
    draw.circle((3, 3.5), radius: 0.3, fill: rgb("#f4a460"))
    draw.line((3, 3.5), (3, 5), stroke: 2pt + rgb("#2ecc71"))
    draw.circle((3, 5.5), radius: 0.8, fill: rgb("#2ecc71"))
  })
]
#v(0.5cm)

One spring morning, the sun whispered, "Wake up, little one."

#pagebreak()

And so the seed began to grow...
```

Compile:
```bash
typst compile book.typ tiny-seed.pdf
```
