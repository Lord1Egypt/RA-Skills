---
name: slide-generation
description: >-
  Generate Marp teaching slides from source content for teachers. Use when:
  (1) Generating Marp-compatible markdown slides from a .md file or folder for teaching/presentations,
  (2) Creating course slides with specific themes (am_blue_course), headers (logo), footers (敬业乐群), and presenter info,
  (3) Converting educational content (chapters, notes, multiple sources) into slide format,
  (4) Synthesizing multiple sources into a unified slide deck.
  NOT for: general document editing, non-Marp presentations.
---

# Slide Generation Skill

Generate Marp slides from source content following the AM Blue Course theme and workflow rules.

## Quick Start

1. **Identify sources**: Read all source `.md` files (or all `.md` files in a folder)
2. **Read references**: Load `references/rules.md` and `references/marp-guide.md` before generating
3. **Design structure**: Plan slide sections from source content
4. **Generate**: Output `.md` file with Marp format

## Input Modes

### Single File
```
User: 生成关于"记忆与检索"的幻灯片，基于第八章.md
→ Read 第八章.md, generate slides
```

### Multiple Files / Folder
```
User: 把这个文件夹里的内容整合成一组教学幻灯片
→ Read all .md files in the folder, merge by topic/chapter, generate unified slides
```

When multiple sources are provided:
- Merge content by topic or chapter sequence
- Avoid duplicate content across sources
- If sources conflict, prefer the more recent or comprehensive one

## Output Target

When user specifies an output path (e.g. `chapter8/memory-slide.md`):
1. Create the output folder (e.g. `chapter8/`)
2. Copy all used images to `chapter8/images/`
3. Write the slide markdown to `chapter8/memory-slide.md`

Image path mapping:
- Source path: `../images/xxx.png` → Output path: `./images/xxx.png`
- Copy source images to the output `images/` folder alongside the slide file

## Marp YAML Header (Required)

Always use this exact header:

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

## Required Slide Structure

### 1. Cover Page (First Slide)

```markdown
<!-- _class: cover_c -->
<!-- _paginate: "" -->
<!-- _footer: 敬业乐群 -->
<!-- _header: ![](images/logo.png) -->

###### [Subtitle]

# [Main Title]

@PresenterName
<Email>
```

Subtitle format: use `######` (level 6 heading)
Main title: use `#` (level 1 heading)

### 2. Table of Contents (Second Slide)

```markdown
## 本节内容

<!-- _class: toc_a -->
<!-- _header: "CONTENTS" -->
<!-- _footer: 敬业乐群 -->
<!-- _paginate: "" -->

- [Topic 1](#3)
- [Topic 2](#N)
- ...
```

### 3. Content Slides

Use `##` (level 2 heading) for main section titles. The `headingDivider: [2,3]` setting automatically splits pages at `##` and `###` headings.

For content-heavy pages, apply text-size classes:
- `<!-- _class: smalltext -->` — 0.9x font size
- `<!-- _class: tinytext -->` — 0.8x font size

For narrow/wide images, avoid left-right layouts; use full-width instead.

## Core Rules

### Must Follow

- ✅ Content must come ONLY from source files — do not add external knowledge
- ✅ Keep content rich but within source bounds
- ✅ Preserve original images from source; copy to output `images/` folder
- ✅ Use `logo.png` as header image (path: `images/logo.png` in output)
- ✅ Presenter name and email as specified by user
- ✅ Use `<!-- *class: smalltext* -->` or `<!-- *class: tinytext* -->` for dense content
- ✅ Inline math: wrap in `$...$` (e.g. `$f(x) = y$`)
- ✅ Convert code to pseudocode if it aids comprehension
- ✅ Section numbering: use `2.2` not `10.2.2`; omit chapter prefix

### Must NOT

- ❌ Use classes not defined in theme files
- ❌ Use transition slides (`<!-- _class: trans -->`)
- ❌ Use `---` for manual page breaks (headingDivider already handles this)
- ❌ Title encoding like `10.2.2` — use `2.2` instead
- ❌ Generate images — only use images from source content

## Layout Decision Rules

Based on image/table shape:

| Content Shape | Recommended Layout |
|---|---|
| Wide image (aspect < 1:1) | Full-width, no columns |
| Tall image (aspect > 1:1) | Left-right columns possible |
| Square image | Flexible, consider columns |
| Tables | Full-width or right-aligned; avoid narrow columns |
| Code blocks | Full-width, consider `tinytext` |
| Mixed text + image | Use `cols-2` (五五分) or `cols-2-64` (六四分) |

Image scaling: use `![#c w:700](path)` or `![#c h:300](path)` to adjust size dynamically.

### Column Layout Examples

**Two columns (五五分)**:
```markdown
<!-- _class: cols-2 -->
<div class=ldiv>

Left column content
</div>

<div class=rdiv>

Right column content
</div>
```

**Two columns (六四分, image on left)**:
```markdown
<!-- _class: cols-2-64 -->
<div class=limg>

![#c](image.png)
</div>

<div class=rdiv>

Right column text
</div>
```

**fig-top layout (image on top)**:
```markdown
<!-- _class: fig-top -->
<div class=fig-container>

![width:850px](image.png)
</div>

<div class=text-container>

Content text
</div>
```

## Available Classes

Reference: `assets/example_file/AwesomeMarp_blue.md` and `assets/example_file/slide.md`

**Page layout**: `cols-2`, `cols-2-64`, `cols-2-73`, `cols-2-46`, `cols-2-37`, `cols-3`, `rows-2`, `pin-3`

**Text size**: `tinytext`, `smalltext`, `largetext`, `hugetext`

**Special**: `toc_a`, `cover_c`, `fig-top`, `fglass`, `caption`, `fixedtitleA`, `fixedtitleB`

**Callouts**: `bq-purple`, `bq-blue`, `bq-green`, `bq-red`, `bq-black`

## Image Handling

1. Scan source for `![]()` image syntax
2. Copy each image file to output `images/` folder
3. In slide markdown, reference images relative to output location: `![](images/filename.png)`
4. Map original paths (e.g. `../images/8-figures/8-1.png`) to new paths (`images/8-1.png`)

For logos and theme images, use: `images/logo.png` (copied from `assets/images/logo.png`)

## Multi-Source Synthesis

When synthesizing from multiple sources:

1. **Read all sources first** — get full picture of content
2. **Identify overlap** — note repeated topics across files
3. **Deduplicate** — consolidate overlapping content
4. **Merge by structure**:
   - If sources are chapters of the same book → follow chapter order
   - If sources are different perspectives → create unified section structure
   - If sources have conflicting info → prefer user's stated preference or most recent
5. **Generate one coherent slide deck** — unified structure, consistent style

## Quality Checklist

Before finishing, verify:
- [ ] YAML header matches required format exactly
- [ ] Cover page has all: main title, subtitle, presenter name, email, logo, footer, no page number
- [ ] TOC page links to correct slide numbers
- [ ] All images from source are included and copied to `images/` folder
- [ ] No Marp classes used beyond what's in theme files
- [ ] No `---` page breaks (headingDivider handles it)
- [ ] Inline math uses `$...$` syntax
- [ ] No title encodings like `10.2.2` — use `2.2`
- [ ] Content stays within source material bounds
- [ ] Logo path is `images/logo.png`
