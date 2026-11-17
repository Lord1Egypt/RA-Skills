## Description:

技术方案文档智能体：输入技术选型要点，自动生成方案对比、架构图和评审检查清单

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahsh](https://clawhub.ai/user/mahsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to research and compare technical options, draft cloud phone architecture proposals, and prepare actionable review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposal keywords may include confidential project details that are sent to search services or a configured Dify service.

Mitigation: Use only keywords approved for those services; omit confidential details unless the services are approved to receive them.

Risk: A referenced local path could not be resolved during scanning, so the benign scan did not inspect every reference.

Mitigation: Review the full skill and its referenced files before deployment.

## Reference(s):

- [Tech Design Doc Generator on ClawHub](https://clawhub.ai/mahsh/skills/tech-design-doc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Architecture diagram descriptions]

**Output Format:** [Markdown with comparison tables, Mermaid or SVG architecture descriptions, implementation plans, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured proposal document with a recommended option and review checklist.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
