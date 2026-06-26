---
name: svg-architecture-diagram
description: >-
  Create professional, publication-quality technical architecture diagrams using
  pure SVG in HTML, then screenshot via Playwright. Produces crisp, pixel-perfect
  diagrams with precise connection lines, color-coded modules, and clear text at
  any resolution. Use when: (1) user asks for a system architecture diagram,
  (2) user wants a technical component diagram or flow chart, (3) user needs a
  data flow or pipeline visualization, (4) any diagram requiring accurate text
  labels and precise connecting lines. Triggers: "architecture diagram",
  "架构图", "技术架构", "system diagram", "component diagram", "flow diagram",
  "数据流图", "模块图", "draw architecture", "画架构图", "technical diagram".
  Prefer this over AI image generation for any diagram with text labels.
---

# SVG Architecture Diagram

Create professional technical architecture diagrams using pure SVG, rendered to high-res PNG via Playwright.

## Why SVG (not CSS positioning or AI image generation)

| Approach | Lines/Arrows | Text Quality | Precision |
|----------|-------------|-------------|-----------|
| **SVG (this skill)** | ✅ Perfect: `<line>`, `<path>`, `<marker>` | ✅ Crisp at any size | ✅ Pixel-perfect |
| CSS absolute positioning | ❌ Hacky: borders, pseudo-elements | ✅ OK | ❌ Hard to align |
| AI image generation | ❌ No control | ❌ Garbled text | ❌ No precision |

## Quick Start

### Step 1: Plan the diagram

Identify:
- **Modules** — group related components (color-coded)
- **Hierarchy** — top-to-bottom flow (user → core → subsystems → output)
- **Connections** — data flow (solid lines), feedback (dashed lines)

### Step 2: Create the HTML file

Write a single HTML file with an inline SVG. Standard canvas: **1600×1000px**.

```html
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1600px; height: 1000px; background: #fafafa; overflow: hidden; }
</style>
</head><body>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" width="1600" height="1000">
  <defs>
    <!-- Arrow markers — one per color -->
    <marker id="arr-indigo" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6 Z" fill="#6366f1"/>
    </marker>
    <!-- Shadow filter -->
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Diagram content here -->

</svg>
</body></html>
```

### Step 3: Build the diagram using these SVG patterns

**Filled header card** (module title):
```svg
<rect x="X" y="Y" width="W" height="40" rx="10" fill="#6366f1" filter="url(#shadow)"/>
<text x="CENTER" y="Y+25" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">🔄 Module Name</text>
```

**Outlined detail card** (sub-component):
```svg
<rect x="X" y="Y" width="W" height="65" rx="10" fill="#fff" stroke="#6366f1" stroke-width="2" filter="url(#shadow)"/>
<text x="X+20" y="Y+22" font-size="12" font-weight="700" fill="#6366f1">Component Title</text>
<text x="X+20" y="Y+40" font-size="11" fill="#6b7280">Description line 1</text>
<text x="X+20" y="Y+55" font-size="10" fill="#9ca3af">Metadata / specs</text>
```

**Connection line** (with arrow):
```svg
<line x1="FROM_X" y1="FROM_Y" x2="TO_X" y2="TO_Y" stroke="#6366f1" stroke-width="2" marker-end="url(#arr-indigo)"/>
```

**Curved connection** (L-shape or bend):
```svg
<path d="M startX,startY L midX,midY L endX,endY" stroke="#6366f1" stroke-width="2" fill="none" marker-end="url(#arr-indigo)"/>
```

**Dashed feedback line**:
```svg
<path d="M x1,y1 L x2,y2" stroke="#8b5cf6" stroke-width="2" fill="none" stroke-dasharray="6,4" marker-end="url(#arr-purple)"/>
```

**Connection label**:
```svg
<text x="MID_X" y="MID_Y-5" font-size="10" fill="#6366f1" font-weight="500">label text</text>
```

### Step 4: Screenshot with Playwright

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 1600, "height": 1000},
        device_scale_factor=4,  # 4x ultra-high res (default)
    )
    page.goto("file:///path/to/diagram.html", wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.screenshot(path="diagram.png", full_page=True)
    browser.close()
```

Or use the bundled script: `scripts/screenshot.py <input.html> [output.png]`

## Design System

See `references/design-system.md` for the complete color palette, card styles, arrow markers, and text sizing rules.

## Critical Rules (prevent common issues)

### Text Overflow Prevention
1. **Max characters per line** at font-size 11px ≈ 7px/char:
   - 300px container → max 37 chars
   - 340px container → max 43 chars
   - 440px container → max 57 chars
2. **Long text → split into multiple `<text>` elements** with Y offset +15px each
3. **Always leave 20px padding** on each side of text inside cards
4. **Test at 1x scale** before generating final 4x screenshot

### Connection Line Rules
1. **Never use CSS for connections** — always SVG `<line>` or `<path>`
2. **One `<marker>` per color** — define in `<defs>`, reference with `marker-end`
3. **Straight lines** when possible; use `<path>` L-segments for bends
4. **Avoid crossing lines** — rearrange layout if lines would cross
5. **Label every connection** — brief verb/noun near the midpoint
6. **⚠️ Minimum 20px gap between vertically stacked cards** — Arrow markers are 8px long. If the gap between cards is less than 20px, the arrow will completely cover the line, making it look like "arrow only, no line". Use card height 34px + gap 22px = 56px per step.
7. **Connection line length must be at least 17px** — This ensures 9px visible line + 8px arrow marker. Example: card bottom at y=324, next card top at y=346, line from y1=324 to y2=343 (19px).
8. **Never make line length < marker size (8px)** — The line will be invisible.

### Layout Rules
1. **Top-to-bottom** primary flow (input at top, output at bottom/right)
2. **Left-right symmetry** when possible
3. **Group related modules** vertically (e.g., memory layers stacked)
4. **Minimum 20px gap** between vertically stacked cards (see Connection Line Rules)
5. **Color-code by function** — see design system for standard palette
6. **Include a legend** (bottom-right corner) explaining colors and line types
7. **Include a title** (top center) and source attribution (bottom center)

### Font Rules
1. **Font family**: `font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif"` — set on root `<svg>` or first `<text>`
2. Load Inter via Google Fonts in `<style>` block
3. **Chinese text**: use `PingFang SC` / `Microsoft YaHei` fallback
4. **Font sizes**: titles 13-14px, descriptions 10-11px, metadata 9-10px

## Examples

Two complete working examples are included:

- `references/example-hermes.html` — Hermes Agent architecture (6 modules, medium complexity)
- `references/example-openclaw.html` — OpenClaw platform architecture (12 modules, high complexity, demonstrates proper vertical card spacing for Agent Loop steps)

## Delivery

Output `MEDIA:<path>` for inline delivery, or `openclaw message send --channel telegram --target <id> --media <path> --force-document` for Telegram.

If PNG exceeds ~1MB for Telegram delivery, convert to JPEG (quality=95):

```python
from PIL import Image
img = Image.open("diagram.png")
img.save("diagram.jpg", "JPEG", quality=95, optimize=True)
```

Default is 4x (6400×4000px for 1600×1000 canvas). Always use maximum resolution.
