## Description:

Converts architecture diagrams or infrastructure plans into infrastructure as code, deployment manifests, workflow code, or component code with assumptions and node-to-resource mappings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn Mermaid, PlantUML, draw.io XML, ASCII, or text-described architecture diagrams into deployable infrastructure definitions, workflow scripts, or component code. It is intended for diagram-backed requests where assumptions and mappings can be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scaffolded README workflows mention API keys and write modes without documenting the backing service or exact file changes.

Mitigation: Do not provide API keys or run write-mode workflows unless the publisher documents the service used and the files that will be changed.

Risk: Generated infrastructure or component code may include incorrect defaults or assumptions when the source diagram is incomplete.

Mitigation: Review the node-to-resource mapping, assumptions, and generated configuration before deployment or integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/wangjipeng-diagram-to-code)
- [Declared metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and diagram-to-code mapping notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and refinement prompts for ambiguous diagram elements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
