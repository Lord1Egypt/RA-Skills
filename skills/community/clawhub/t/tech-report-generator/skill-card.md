## Description:

Generates beginner-friendly deep technical reports from a technical topic, producing structured Markdown and HTML with SVG visualizations and sync workflows for IMA Knowledge Base and Tencent Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fandywang87](https://clawhub.ai/user/fandywang87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and training authors use this skill to turn technical topics into onboarding, tutorial, and knowledge-sharing reports with structured explanations and visual diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain internal architecture, benchmarks, roadmap details, personal data, or secrets.

Mitigation: Review report content before any synchronization step and require explicit approval before publishing sensitive material.

Risk: The skill can publish generated content to external Tencent/IMA services using local credentials without a clear approval gate.

Mitigation: Require explicit local-only or publish confirmation, and verify the IMA knowledge base, Tencent Docs destination, and credential scope before synchronization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fandywang87/skills/tech-report-generator)
- [Report Structure Template](references/report-template.md)
- [SVG Visualization Design Guide](references/svg-design-guide.md)
- [Synchronization Workflow Reference](references/sync-workflow.md)
- [HTML Report Template](assets/html-template.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and HTML reports with inline SVG diagrams and optional synchronization commands or tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include report metadata, tables, pseudocode, SVG visualizations, and distribution steps for IMA Knowledge Base or Tencent Docs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
