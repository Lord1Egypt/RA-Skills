# SVG Architecture Diagram — Color Palette Reference

## Standard Module Colors

| Module Type | Fill Color | Border | Text | Use For |
|-------------|-----------|--------|------|---------|
| User / External | `#ec4899` (pink) | — | white | User input, LLM, external services |
| Core Engine | `#6366f1` (indigo) | — | white | Main loop, core processing, orchestration |
| Storage / Memory | `#10b981` (green) | `#10b981` | green/gray | Database, cache, memory layers |
| Plugin / Extension | `#f59e0b` (amber) | `#f59e0b` | amber/gray | Skills, plugins, extensions |
| AI / Learning | `#8b5cf6` (purple) | `#8b5cf6` | purple/gray | Self-evolution, ML, optimization |
| Infrastructure | `#64748b` (slate) | `#94a3b8` | slate/gray | Tools, shell, file system |
| Security / Guard | `#ef4444` (red) | `#ef4444` | red | Security, validation, guard |
| Output / Result | `#10b981` (green) | — | white | Output, delivery, response |

## Card Styles

### Filled Card (header/title blocks)
```svg
<rect x="X" y="Y" width="W" height="40" rx="10" fill="#6366f1" filter="url(#shadow)"/>
<text x="CENTER" y="Y+25" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">Title</text>
```

### Outlined Card (detail blocks)
```svg
<rect x="X" y="Y" width="W" height="H" rx="10" fill="#fff" stroke="#6366f1" stroke-width="2" filter="url(#shadow)"/>
<text x="X+20" y="Y+22" font-size="12" font-weight="700" fill="#6366f1">Title</text>
<text x="X+20" y="Y+40" font-size="11" fill="#6b7280">Description</text>
<text x="X+20" y="Y+55" font-size="10" fill="#9ca3af">Metadata</text>
```

### Highlight Card (warnings/special)
```svg
<rect x="X" y="Y" width="W" height="H" rx="10" fill="#fffbeb" stroke="#f59e0b" stroke-width="1"/>
```

## Arrow Markers

```svg
<marker id="arr-indigo" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <path d="M0,0 L8,3 L0,6 Z" fill="#6366f1"/>
</marker>
```

## Connection Lines

| Type | Style | Use |
|------|-------|-----|
| Data flow | `stroke-width="2"` solid + arrow | Primary data movement |
| Feedback | `stroke-width="2" stroke-dasharray="6,4"` + arrow | Feedback loops, optimization |
| Internal | `stroke-width="1.5"` solid + arrow | Within-module connections |
| Label | `font-size="10" font-weight="500"` | Connection description |

## Text Sizing Rules

| Element | Font Size | Weight | Anchor |
|---------|-----------|--------|--------|
| Page title | 22px | 700 | middle |
| Subtitle | 12px | 400 | middle |
| Module header | 13-14px | 700 | middle |
| Card title | 11-12px | 700 | left |
| Description | 10-11px | 400 | left |
| Metadata | 9-10px | 400 | left |
| Connection label | 10px | 500 | left |
| Legend | 11px | 400 | left |

## Anti-Overflow Rules

1. **Max text width** = container width - 40px (20px padding each side)
2. At 11px font, ~7px per character → max ~43 chars in 300px container
3. Long text → split into two `<text>` lines (Y offset +16px)
4. Use `text-anchor="middle"` for centered headers
5. Use left-aligned for descriptions in outlined cards

## Card Spacing Rules (CRITICAL)

1. **Vertical stacked cards**: card height 34px + gap 22px = **56px per step**
2. **Connection line**: start at card bottom (y + height), end at next card top (y) minus 3px
3. **Minimum line length**: 17px (9px visible line + 8px arrow marker)
4. **Arrow marker size**: 8px — if line < 8px, arrow covers entire line (invisible)
5. **Example**: card at y=290 h=34 → bottom=324. Next card y=346. Line: y1=324 y2=343 (19px ✓)
