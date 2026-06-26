# Slide Generation Rules

## Theme Configuration

**Theme files**: `am_blue_course.scss` + `am_template.scss` (always use together)
- `am_blue_course.scss` — course-specific styling (header, footer, colors)
- `am_template.scss` — base layout and typography

**Required YAML**:
```yaml
---
marp: true
size: 16:9
theme: am_blue_course
paginate: true
headingDivider: [2,3]
footer: '*敬业乐群*'
---
```

## Cover Page (cover_c)

```markdown
<!-- _class: cover_c -->
<!-- _paginate: "" -->
<!-- _footer: 敬业乐群 -->
<!-- _header: ![](images/logo.png) -->

###### [Subtitle - level 6 heading]

# [Main Title - level 1 heading]

@PresenterName
<Email@example.com>
```

## Table of Contents (toc_a)

```markdown
## 本节内容

<!-- _class: toc_a -->
<!-- _header: "CONTENTS" -->
<!-- _footer: 敬业乐群 -->
<!-- _paginate: "" -->

- [Section 1](#3)
- [Section 2](#N)
```

## Header Image (Logo)

- Source: `assets/images/logo.png`
- In output: `images/logo.png` (copy to output folder)
- Usage: `<!-- _header: ![](images/logo.png) -->`

## Presenter Info

- Name: from user's request
- Email: from user's request
- Footer text: **敬业乐群** (always, Chinese)

## Content Rules

### Text Size Classes

| Class | Effect |
|-------|--------|
| `tinytext` | 0.8x default font size |
| `smalltext` | 0.9x default font size |
| `largetext` | 1.15x default font size |
| `hugetext` | 1.3x default font size |

Apply to content-heavy pages: `<!-- _class: smalltext -->`

### Layout Classes (from am_template/am_blue)

**Two columns**:
- `cols-2` — 五五平分
- `cols-2-64` — 六四分 (left 60%, right 40%)
- `cols-2-73` — 七三分 (left 70%, right 30%)
- `cols-2-46` — 四六分 (left 40%, right 60%)
- `cols-2-37` — 三七分 (left 30%, right 70%)

**Three columns**: `cols-3`

**Two rows**: `rows-2`

**Pin layout**: `pin-3` (品字型)

**Image column alignment**:
- `<div class=ldiv>` — left column, top-aligned
- `<div class=limg>` — left column, center-aligned (for images)
- `<div class=rdiv>` — right column, top-aligned
- `<div class=rimg>` — right column, center-aligned (for images)

### fig-top Layout (Image on Top)

```markdown
<!-- _class: fig-top -->
<div class=fig-container>

![width:850px](image.png)
</div>

<div class=text-container>

Content text here
</div>
```

### Image Sizing

- `![#c w:700](path)` — center image, width 700px
- `![#c h:300](path)` — center image, height 300px
- `![width:850px](path)` — explicit width

Use scaling to optimize layout — do not force wide images into narrow columns.

## Mathematical Formulas

Inline math: `$...$`
Example: `$f(x) = \sum_{i=1}^{n} w_i x_i$`

## Title Encoding

❌ Wrong: `10.2.2`, `第三章`
✅ Right: `2.2`, `记忆的主要类型`

## Page Breaking

- DO NOT use `---` for manual page breaks
- `headingDivider: [2,3]` automatically splits at `##` and `###`
- Use `##` for main section titles
- Use `###` for subsections within a slide page

## Forbidden

- ❌ `<!-- _class: trans -->` (transition slides)
- ❌ `---` (manual page break)
- ❌ Classes not in theme (e.g. custom invented classes)
- ❌ Generating images not in source content
- ❌ Adding content beyond source material

## Code to Pseudocode

For long code blocks, condense to key logic lines or pseudocode:
```python
# Before: Full implementation code
# After: Key algorithm steps in comments
```

## Output File Structure

```
output_folder/
├── memory-slide.md    # Main slide file
└── images/
    ├── logo.png       # Header logo
    ├── xxx.png        # Source images
    └── ...
```

Image path in markdown: `![](images/filename.png)`
