# Hermes Agent Task: Diagram Generator

## Mission

Create high-quality standalone technical diagrams as HTML files with inline SVG. Activate when the user asks to draw, create, or generate an **architecture diagram, system map, infrastructure diagram, topology diagram, deployment map, data-flow diagram, sequence diagram, process flow, trust boundary, cloud diagram, or draw.io export** — or uses phrases like "帮我画个架构图", "画一张拓扑图", "生成系统图", "画个时序图", "画个部署图", "画个流程图", "show me the system map", "map out the architecture", or "diagram this".

## Context Files

- `resources/generation-rules.md`
- `resources/diagram-ir.md`
- `resources/template.html`

## Execution Steps

1. Read the user's brief.
2. Normalize the brief into components, boundaries, flows, risks, and assumptions.
3. Use `resources/generation-rules.md` to select the correct lens and output mode.
4. Use `resources/diagram-ir.md` as the planning model before rendering.
5. If editing an existing diagram, inspect the current artifact first and preserve unrelated content, notes, and color semantics.
6. Produce a complete standalone HTML file using `resources/template.html` as the base.
7. Replace every placeholder with concrete content from the brief or a clearly labeled assumption.
8. Run the final audit checklist in `resources/generation-rules.md`, including layout quality, label readability, arrow direction, boundary correctness, mobile behavior, and export controls.

## Completion Criteria

- The diagram opens directly in a browser.
- The diagram explains the system without requiring extra narration.
- Export buttons are present.
- No placeholder text remains.
- Any assumptions are disclosed in the notes rail.

Do not duplicate shared design principles in this platform entrypoint. Keep reusable rules in `resources/generation-rules.md`.
