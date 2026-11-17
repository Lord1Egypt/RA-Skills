# HTML + Draw.io XML Mode Prompt

This is an experimental mode. Generated XML must be import-tested in draw.io before use.

Use the `diagram-generator` skill in html + drawio xml mode.

## Output Requirements

- Generate a standalone `.html` file with inline SVG as the primary rendered diagram.
- Plan the diagram with `resources/diagram-ir.md` before rendering.
- Add a visible control for opening the secondary draw.io XML panel.
- Embed semantically faithful draw.io XML in the HTML page so the user can copy the XML.
- The draw.io XML does not need to reproduce every visual effect exactly, but it should preserve the diagram structure, boundaries, nodes, and principal flows.
- Do not claim draw.io compatibility unless the generated XML was successfully imported and inspected.

## System Brief

- Browser and mobile users access the system through CDN and API gateway.
- Authentication is handled by an external OIDC provider.
- Core services run in Kubernetes.
- PostgreSQL stores transactional data.
- Redis stores sessions and cache data.
- Kafka carries domain events.
- Reporting and media pipelines generate downstream assets.
- Operations include orchestration, smoke tests, and final audits.

## Final Instruction

Return a production-ready HTML document that includes both the visible system map and the embedded draw.io XML export source.
