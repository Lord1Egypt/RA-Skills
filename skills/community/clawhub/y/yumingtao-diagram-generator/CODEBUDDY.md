# CodeBuddy Workspace Rule: Diagram Generator

Use this rule when the user asks to draw, create, or generate an **architecture diagram, system map, infrastructure diagram, topology diagram, deployment map, data-flow diagram, sequence diagram, process flow, trust boundary, cloud diagram, or draw.io export** — or uses phrases like "帮我画个架构图", "画一张拓扑图", "生成系统图", "画个时序图", "画个部署图", "画个流程图", "show me the system map", "map out the architecture", or "diagram this".

Generate a standalone HTML document with inline SVG and embedded styles. Read and follow `resources/generation-rules.md`, `resources/diagram-ir.md`, and `resources/template.html` before generating.

## Behavior

- Parse the user's system description into components and relationships.
- Use `resources/generation-rules.md` as the source of truth for lens selection, design language, layout, output modes, export requirements, and the final audit checklist.
- Use `resources/diagram-ir.md` as the planning model before rendering.
- If editing an existing diagram, inspect the current artifact first and preserve unrelated content, notes, and color semantics.
- Use `resources/template.html` as the implementation base.
- Replace every placeholder with concrete content from the brief or a clearly labeled assumption.
- Run the final audit checklist in `resources/generation-rules.md` before returning.

Do not duplicate shared design principles in this platform entrypoint. Keep reusable rules in `resources/generation-rules.md`.
