---
name: visualize
description: "Use when content needs a diagram or visual — auto-detects content shape, picks the best format per the active-selection rule, and renders it."
---

# /visualize

Auto-detect content shape and render the appropriate visualization. Follows the active-selection rule from `ai-workspace/rules/visualizations.md`.

## Usage

```
/visualize                              # visualize the last discussed concept
/visualize <topic or file>              # visualize specific content
/visualize --format mermaid <topic>     # force a specific format
```

## Steps

1. **Identify content.** From args, recent conversation context, or a file path. Determine what needs visualizing.

2. **Classify content shape.** Use this decision table:

   | Content shape | Signal | Format |
   |---|---|---|
   | Graph with nodes + edges | architecture, dependencies, flow between components | Mermaid `graph` or `flowchart` |
   | Sequence / interaction | request flow, API calls, multi-step protocol | Mermaid `sequenceDiagram` |
   | State transitions | modes, lifecycle, status changes | Mermaid `stateDiagram-v2` |
   | Comparison (3+ items) | options, tradeoffs, feature matrix | Markdown table |
   | Hierarchy / tree | file structure, org chart, simple nesting | ASCII art |
   | Contrast (2 items) | before/after, good/bad, do/don't | Inline pairs |
   | Entity relationships | data model, schema | Mermaid `erDiagram` |

3. **Check render surface.** Mermaid in committed `.md` files renders on iOS/web/GitHub/VS Code. In terminal chunks, Mermaid is literal text — use ASCII instead. When surface is unknown, default to ASCII.

4. **Render.**
   - **ASCII / table / inline pairs**: output directly in the response.
   - **Mermaid**: output as a fenced `mermaid` code block in the response. If high-resolution PNG is needed:
     ```bash
     node --import tsx "${SKILL_DIR}/scripts/render-mermaid.ts" --input <mermaid-file> --output <png-path> --width 2400 --height 1800
     ```
   - **Format override**: if user passed `--format`, use that format regardless of auto-detection.

5. **Present.** Show the visualization. If Mermaid PNG was rendered, display the path.

## Failure modes

| Condition | Behavior |
|---|---|
| Content shape ambiguous | Ask: "This could be a [X] or [Y] — which fits better?" |
| Mermaid syntax error | Show the error, offer to fix |
| mmdc not available | Fall back to fenced Mermaid block (renders on GitHub/web) |

## Cross-tool notes

- **Codex / Cursor**: run `scripts/render-mermaid.ts` directly for PNG rendering. Content-shape detection is agent reasoning, not script logic.
