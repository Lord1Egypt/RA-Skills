---
name: mermaid-to-gif
description: Convert Mermaid code blocks in .mmd or .md files to animated GIFs with customizable animation styles (progressive, highlight walk, pulse flow, wave).
---

# Skill: Mermaid to GIF

Convert Mermaid diagrams into animated GIFs with rich animation effects. Supports `.mmd` files and extracting ` ```mermaid ` code blocks from `.md` files.

> **Prerequisites**: FFmpeg, Python 3.8+, Playwright (`pip install playwright && playwright install chromium`)

---

## When to Use

- The user wants to convert Mermaid diagrams to animated GIFs
- The user has `.mmd` files or `.md` files containing mermaid code blocks
- The user needs animated visuals for presentations, documentation, or social media
- The user wants to batch-convert all mermaid blocks in a document

---

## Context-Aware Style Selection

**IMPORTANT**: When converting mermaid blocks from `.md` files, read the surrounding markdown context to choose the most appropriate animation style for each diagram. Do NOT blindly apply the same style to all blocks.

### Decision Guide

1. **Read the markdown text around each mermaid block** — understand what the diagram is illustrating
2. **Match the style to the semantic meaning**:

| Context Clue | Recommended Style | Reasoning |
|--------------|------------------|-----------|
| Data pipeline, ETL flow, request/response path | `pulse-flow` | Flowing dashed lines convey data movement |
| Architecture layers, org chart, hierarchy | `progressive` | Elements activate layer-by-layer |
| Step-by-step process, tutorial walkthrough | `highlight-walk` | Spotlight guides the reader through each step |
| System overview, title diagram, simple reference | `wave` | Brightness ripple adds life without distraction |
| Sequence diagram with message flow | `progressive` | Messages activate one by one in conversation order |
| Class/ER diagram (reference/static) | `progressive` or `wave` | Structure lights up or gets a subtle ripple |

3. **Consider special handling**:
   - If the surrounding text says "data flows from A to B", use `pulse-flow` even for a simple flowchart
   - If the text describes "three layers" or "two tiers", use `progressive` to activate layer-by-layer
   - If the diagram is decorative or supplementary, use `wave` to keep it simple
   - For very large or complex diagrams, prefer `wave` or shorter `--duration` to keep GIF size reasonable

4. **Per-block style override**: When batch-processing a `.md` file, you may need to run the script multiple times with different styles, extracting specific blocks. Or process the whole file with a sensible default and re-run individual blocks that need different treatment.

### Example: Context-Aware Processing

```markdown
## Data Ingestion Pipeline        ← context: "pipeline" → pulse-flow
[mermaid block: graph LR with ETL stages]

## System Architecture            ← context: "architecture" → progressive
[mermaid block: graph TD with layers]

## Quick Reference                ← context: "reference" → wave
[mermaid block: simple diagram]
```

---

## Default Workflow

### Single .mmd file

```bash
python <skill-root>/scripts/mermaid_to_gif.py diagram.mmd
```

### Markdown file with mermaid blocks

```bash
python <skill-root>/scripts/mermaid_to_gif.py document.md -o ./images/
```

This extracts all ` ```mermaid ` code blocks and generates one GIF per block.

### Multiple files

```bash
python <skill-root>/scripts/mermaid_to_gif.py *.mmd -o ./gifs/
python <skill-root>/scripts/mermaid_to_gif.py doc1.md doc2.md -o ./gifs/
```

### Replacing mermaid blocks in markdown

After generating GIFs, replace the original ` ```mermaid ` code blocks with image references:

```markdown
![Flow Diagram](images/document-1.gif)
```

Use descriptive alt text based on the diagram content. The image path should be relative to the markdown file.

---

## Animation Styles

All styles keep the diagram **fully visible from frame 1** — no elements start hidden or fade in from zero. Every style adds motion while the user can see the complete diagram structure at all times.

| Style | Effect | Best For |
|-------|--------|----------|
| `progressive` (default) | All elements start dimmed (25% opacity), activate sequentially to full brightness; edges draw in with stroke animation | Flowcharts, architecture, hierarchy |
| `highlight-walk` | All elements start dimmed (15%); a spotlight with blue glow moves through each element, leaving visited ones bright | Step-by-step process, tutorials |
| `pulse-flow` | All elements fully visible; edges become flowing dashed lines (uniform dash size and speed) | Data flow, pipelines, request paths |
| `wave` | All elements fully visible; a brightness pulse + blue glow ripple sweeps through elements sequentially | Simple diagrams, overviews, reference |

### Animation Details

- **progressive**: Elements start at 25% opacity (diagram structure always visible). Nodes, edges, and labels activate in interleaved order (node → edge → node → edge) following flow direction. Edges use stroke-dashoffset to draw in visually. Activation is fast (8% of total duration per element).
- **highlight-walk**: All elements start at 15% opacity. A spotlight (with blue glow) moves through elements in order, leaving visited elements at 90% opacity. The whole diagram is visible as a "ghost" before the spotlight reaches each element.
- **pulse-flow**: All elements at full opacity. Edge paths get a uniform dashed pattern (10px dash + 6px gap) that flows at a fixed speed (200px/cycle), so all edges animate at the same pace regardless of length.
- **wave**: All elements at full opacity. A brightness pulse (1.0→1.4→1.0) with blue glow sweeps through elements sequentially. No position changes — purely a visual ripple effect.

---

## Common Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output-dir` | Same as input | Output directory for generated GIFs |
| `-s`, `--style` | `progressive` | Animation style (see table above) |
| `--fps` | `10` | Frames per second |
| `--duration` | `4.0` | Animation duration in seconds |
| `--hold` | `1.0` | Hold last frame before looping (seconds) |
| `--theme` | `default` | Mermaid theme: default, dark, forest, neutral |
| `--bg` | `#ffffff` | Background color (hex) |
| `--padding` | `40` | Padding around diagram in pixels |
| `--scale` | `2` | Render scale factor (2 = retina quality) |
| `--custom-css` | — | Path to custom CSS file |
| `--no-loop` | — | Play GIF once instead of looping |

---

## Examples

```bash
# Dark theme with faster animation
python <skill-root>/scripts/mermaid_to_gif.py arch.mmd --theme dark --bg "#1a1a2e" --duration 3

# High FPS for smoother animation
python <skill-root>/scripts/mermaid_to_gif.py flow.mmd --fps 15 --duration 5

# Batch convert all mermaid blocks from a doc
python <skill-root>/scripts/mermaid_to_gif.py README.md -o ./images/

# Custom CSS for special effects
python <skill-root>/scripts/mermaid_to_gif.py diagram.mmd --custom-css my-style.css

# No loop, suitable for one-time playback
python <skill-root>/scripts/mermaid_to_gif.py intro.mmd --no-loop --duration 6

# Lower resolution for smaller file size
python <skill-root>/scripts/mermaid_to_gif.py diagram.mmd --scale 1
```

---

## Custom CSS

Create a CSS file to customize the appearance of the diagram during animation:

```css
/* Rounded nodes with shadow */
.node rect {
    rx: 10;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
}

/* Thicker edge lines */
.edgePath path {
    stroke-width: 2.5;
}

/* Custom background for actors (sequence diagram) */
.actor {
    fill: #e8f4f8;
}
```

Pass it via `--custom-css`:

```bash
python <skill-root>/scripts/mermaid_to_gif.py diagram.mmd --custom-css my-style.css
```

---

## How It Works

1. **Parse input** — extract Mermaid code from `.mmd` or `.md` files
2. **Generate HTML** — embed Mermaid.js (CDN) + animation JS/CSS in a self-contained HTML file
3. **Render** — Mermaid.js renders the diagram to SVG in headless Chromium via Playwright (with 2x device scale for retina quality)
4. **Scale** — small SVGs are automatically scaled up to minimum 700px CSS width for readability
5. **Animate** — JS animation engine exposes `setProgress(t)` for frame-by-frame control (t: 0→1). Elements are collected, sorted by position (respecting LR/TB direction), and animated in interleaved node-edge order
6. **Capture** — Playwright takes a screenshot at each frame step
7. **Assemble** — FFmpeg two-pass palette encoding (palettegen → paletteuse with Floyd-Steinberg dithering)

---

## Important Notes

- **Internet required**: Mermaid.js is loaded from CDN at render time
- **Supported diagram types**: flowchart, sequence, class, state, ER, gitgraph, mindmap, pie, gantt, and more
- **No hidden elements**: all 4 styles keep the diagram visible from frame 1 — no waiting for elements to appear
- **Fallback behavior**: for unrecognized diagram types or when no animatable elements are detected, falls back to a whole-diagram opacity reveal
- **Resolution**: default scale=2 produces retina-quality images (~1400-1600px wide). Use `--scale 1` for smaller files
- **GIF size**: for very large outputs, reduce FPS to 8, shorten duration, use `--scale 1`, or use `wave` style
