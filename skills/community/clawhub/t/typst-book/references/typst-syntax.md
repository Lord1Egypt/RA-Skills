# Typst Syntax Quick Reference

## Modes
- **Markup** (default): Text with lightweight syntax
- **Code**: Prefix with `#`
- **Math**: Surround with `$..$`

## Markup Elements

| Element | Syntax |
|---|---|
| Heading | `= Heading`, `== Sub` |
| Bold | `*bold*` |
| Italic | `_italic_` |
| Bullet list | `- item` |
| Numbered list | `+ item` |
| Term list | `/ Term: desc` |
| Link | `https://..` (auto) |
| Label | `<label>` |
| Reference | `@label` |
| Math inline | `$x^2$` |
| Math block | `$ x^2 $` (spaces) |
| Line break | `\` |
| Raw text | `` `code` `` |
| Comment | `// line`, `/* block */` |
| Escape | `\#`, `\$`, `\u{1f600}` |

## Set Rules
```typst
#set page(width: 21cm, height: 29.7cm, margin: 2cm)
#set text(font: "DejaVu Serif", size: 12pt)
#set par(justify: true, leading: 0.8em)
#set heading(numbering: "1.")
```

## Show Rules
```typst
#show heading: it => [custom]
#show figure.where(kind: image): it => [#it]
#show link: it => [#text(fill: blue)[#it]]
```

## Scripting
```typst
#let name = "Ada"
#let greet(name) = [Hello, #name!]
#if name == "Ada" { .. } else { .. }
#for i in range(5) { .. }
#include "chapter.typ"
#import "lib.typ": func1, func2
```

## Layout Functions
- `#align(center)[..]` — alignment
- `#box[..]` / `#block[..]` — containers
- `#grid(columns: 2, ..)` — grid layout
- `#stack(dir: ttb, ..)` — stack layout
- `#place(center + horizon, ..)` — absolute position
- `#v(2cm)` / `#h(1cm)` — spacing
- `#pagebreak()` — page break
- `#colbreak()` — column break

## Figures
```typst
#figure(image("img.png", width: 80%), caption: [Description])
#figure(table(..), caption: [Data])
#outline(title: [Contents])
```

## Visualize (native shapes)
- `#rect(width, height, fill: ..)`
- `#circle(radius: r, fill: ..)`
- `#ellipse(rx, ry, fill: ..)`
- `#square(size, fill: ..)`
- `#line(start: .., end: .., stroke: ..)`
- `#polygon(..points, fill: ..)`
- `#gradient.linear(..colors)`
