## Description:

Smart Charts turns CSV, TSV, TXT, Excel, or JSON tabular data into standalone offline interactive ECharts HTML charts with embedded fact sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-focused agents use this skill to convert supplied tabular files into interactive HTML charts, choose among supported chart types, and return captions grounded in the generated plot statistics. It is not intended for narrative reports, slide decks, backend dashboards, or non-tabular media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pandas/numpy transform code is executed locally in-process with weak resource containment.

Mitigation: Review transform code before execution and use subprocess or container isolation with CPU and memory limits in shared or production environments.

Risk: Untrusted or unexpectedly large tabular inputs can increase parsing and transform risk.

Mitigation: Use trusted input files, keep output directories explicit, and avoid files outside the documented size and format boundaries.

## Reference(s):

- [Smart Charts reference](artifact/references/REFERENCE.md)
- [ClawHub skill page](https://clawhub.ai/neuhanli/skills/smart-charts)

## Skill Output:

**Output Type(s):** [HTML files, JSON summaries, Shell commands, Guidance]

**Output Format:** [Standalone interactive HTML charts with JSON CLI output and concise Markdown delivery text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Charts are generated offline with bundled ECharts assets; successful runs include data previews and plot statistics for caption grounding.]

## Skill Version(s):

8.3.1 (source: SKILL.md frontmatter, server release metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
