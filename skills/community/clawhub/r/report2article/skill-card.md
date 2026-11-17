## Description:

Transforms completed research reports into reader-oriented articles by restructuring sections, prose, titles, and optional visuals while preserving the original facts, evidence, sources, relationships, and judgment strength.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, analysts, editors, and agents use this skill to turn completed Chinese-language research reports, weekly reports, or research notes into readable articles without adding new research or unsupported conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The edited article could omit independent information, alter numbers or dates, or change source attribution or judgment strength.

Mitigation: Build an atomic information checklist before editing and perform both forward coverage and reverse traceability checks before delivery.

Risk: Long reports may be written to local Markdown files, and explicitly requested visuals may create asset files in the agent workspace.

Mitigation: Use the skill only on reports that are acceptable to process in the workspace, and review generated Markdown and asset files before sharing or publishing.

Risk: Visuals can imply unsupported data, relationships, or conclusions if they go beyond the source report.

Mitigation: Use only report-backed data and relationships, label conceptual visuals as illustrative, and include captions, sources, and alt text for generated visuals.

## Reference(s):

- [Atomic Information and Bidirectional Review Template](references/info-checklist-template.md)
- [Article Structure and Section Design](references/logic-skeleton.md)
- [Long Report Processing Protocol](references/long-report-protocol.md)
- [Reader-Oriented Prose and Style](references/prose-style.md)
- [Objective Title Rules and Rewrite Examples](references/title-rules.md)
- [Article Visual Guidelines](references/visual-guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown article text, optional local Markdown files and article asset files, and a concise traceability check statement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short reports are returned inline; long reports may be written to a local Markdown file with optional article assets when explicitly requested and supported.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
