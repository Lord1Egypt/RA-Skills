# GitHub Copilot Custom Instructions: Diagram Generator

When the user asks to draw, create, or generate a diagram, system map, architecture diagram, infrastructure diagram, topology diagram, deployment map, data-flow diagram, sequence diagram, process flow, trust boundary, cloud diagram, or draw.io export — or uses phrases like "帮我画个架构图", "画一张拓扑图", "生成系统图", "画个时序图", "画个部署图", "画个流程图", "show me the system map", "map out the architecture", or "diagram this" — generate a standalone HTML file using inline SVG and embedded CSS. Read and follow `diagram-generator/resources/generation-rules.md`, `diagram-generator/resources/diagram-ir.md`, and `diagram-generator/resources/template.html` before generating.

## Priorities

Use `diagram-generator/resources/generation-rules.md` as the source of truth for behavior, lens selection, output modes, layout rules, and the final audit checklist. Use `diagram-generator/resources/diagram-ir.md` as the planning model before rendering. If editing an existing diagram, inspect the current artifact first and preserve unrelated content, notes, and color semantics. Use `diagram-generator/resources/template.html` as the base HTML/SVG structure. Replace every placeholder with concrete content from the brief or a clearly labeled assumption. Run the final audit checklist from `diagram-generator/resources/generation-rules.md` before returning the file.

## When Editing a Repository

If the user asks you to add a diagram to a repository, create a file under a documentation-friendly location such as `docs/system-map.html` unless the user specifies another path.

Do not duplicate shared design principles in this platform entrypoint. Keep reusable rules in `diagram-generator/resources/generation-rules.md`.
