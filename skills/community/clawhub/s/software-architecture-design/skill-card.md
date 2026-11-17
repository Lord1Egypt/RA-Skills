## Description:

Produces complete software architecture design documents through a 12-phase SOP for web backend, mobile, ML/AI, data pipeline, and embedded/IoT systems, with Mermaid and PlantUML diagram guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1231111](https://clawhub.ai/user/1231111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn requirements, PRDs, RFPs, or verbal system descriptions into structured architecture design documents with MVP scope, architecture decisions, interfaces, deployment, non-functional design, and risk registers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ML/AI architecture guidance may include detailed health endpoints that expose resource status if copied directly into production designs.

Mitigation: Keep public liveness checks minimal and move detailed health and resource reporting to authenticated internal metrics endpoints before production use.

Risk: The default output template is Chinese, which may not match every team's documentation language.

Mitigation: Ask the agent for the required output language at the start of the architecture-design request.

Risk: Architecture proposals can be incomplete or misaligned when requirements are ambiguous.

Mitigation: Resolve the Phase 1 open questions and review generated decisions, diagrams, and risk registers with domain owners before adoption.

## Reference(s):

- [Architecture Design Reference](artifact/reference.md)
- [Architecture Design Document Template](artifact/template.md)
- [Standalone Software Architecture Design SOP](artifact/STANDALONE.md)
- [Web / API Backend Specialization](artifact/specializations/web-backend.md)
- [ML / AI System Specialization](artifact/specializations/ml-system.md)
- [Data Pipeline / Data Platform Specialization](artifact/specializations/data-pipeline.md)
- [Embedded / IoT System Specialization](artifact/specializations/embedded.md)
- [Mobile App Specialization](artifact/specializations/mobile.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown architecture document with Mermaid and PlantUML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output template is Chinese unless the user asks for another language.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
