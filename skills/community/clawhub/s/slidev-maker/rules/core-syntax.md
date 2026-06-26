# Slidev Core Syntax

Fundamental syntax for creating Slidev presentations.

## Slide Separators

Slides are separated by `---` at the start of a line.
```markdown
---
layout: cover
---

# First Slide

Welcome to my presentation

---

# Second Slide

More content here

---

# Third Slide

And so on
```

Use `---` on its own line. Content before the first `---` with frontmatter becomes the first slide.

## Headmatter vs Per-Slide Frontmatter

The FIRST frontmatter block (headmatter) configures the ENTIRE presentation. Per-slide frontmatter configures only that slide.
```markdown
---
# HEADMATTER - applies to entire deck
theme: seriph
title: My Presentation
info: |
  Presentation description here
drawings:
  persist: false
transition: slide-left
mdc: true
---

# First Slide

---
# PER-SLIDE frontmatter - applies only to this slide
layout: center
transition: fade
---

# Second Slide
```

## Common Headmatter Options
```yaml
---
theme: seriph              # Theme name
title: Presentation Title  # Browser tab title
titleTemplate: '%s - Slidev'
info: |                    # Presentation metadata
  Multi-line description
author: Your Name
keywords: slidev,presentation
download: true             # Show download button
exportFilename: my-slides  # Export filename
highlighter: shiki         # Code highlighter (shiki only)
lineNumbers: false         # Code line numbers
monaco: true               # Enable Monaco editor
drawings:
  enabled: true
  persist: false
  presenterOnly: false
  syncAll: true
transition: slide-left     # Default slide transition
mdc: true                  # Enable MDC syntax
---
```

## Common Per-Slide Frontmatter
```yaml
---
layout: center          # Slide layout
class: text-center      # CSS classes for slide
transition: fade        # Override transition for this slide
clicks: 3               # Manual click count
disabled: false         # Disable slide
hide: false             # Hide from presentation
hideInToc: true         # Hide from table of contents
level: 2                # Heading level for TOC
title: Custom Title     # Override title in TOC
preload: false          # Preload slide
zoom: 0.8               # Zoom scale
dragPos:                # Draggable element positions
---
```

## Speaker Notes

Add notes after the slide content using HTML comments.
```markdown
---
layout: default
---

# My Slide

Slide content here.

<!--
These are speaker notes.
They appear in presenter mode.
Can be multiple lines.
-->
```

Notes support Markdown formatting and are visible in presenter mode.

## MDC Syntax

With `mdc: true` in headmatter, use MDC for inline styling.
```markdown
---
mdc: true
---

This is [red text]{style="color: red"}.

This has a [tooltip]{title="Hello!"}.

This is **bold**{.text-blue-500} with a class.
```

## Escaping

To show literal `---` without creating a new slide:
```markdown
Use `\---` to escape the separator.

\---

This stays on the same slide.
```