## Description:

AI半导体工程师 helps semiconductor professionals with device-physics calculations, process and materials reference lookup, IC design and verification guidance, yield and failure analysis, EDA guidance, and HTML report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and semiconductor engineers use this skill to calculate common device parameters, consult process and material reference data, draft IC design and verification guidance, and triage yield or failure-analysis questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web searches for EDA, IC design, process, yield, or failure-analysis questions could expose proprietary chip-design details, process data, tool logs, or yield reports.

Mitigation: Require confirmation before web search and remove confidential design, process, tool-log, and yield details from queries.

Risk: Generated HTML reports may load Chart.js from a CDN, creating an external dependency for sensitive or offline workflows.

Mitigation: Use self-contained reports or pinned and vendored Chart.js when handling confidential semiconductor work.

Risk: Calculator outputs and reference tables use typical values and estimates rather than a specific foundry process specification.

Mitigation: Validate calculations and parameters against process design kits, foundry documentation, or internal specifications before design or manufacturing decisions.

## Reference(s):

- [Semiconductor Materials Data](references/materials_data.md)
- [Semiconductor Process Technology](references/process_technology.md)
- [Semiconductor Device Physics](references/semiconductor_physics.md)
- [Semiconductor Calculator](scripts/semiconductor_calc.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables, calculations, code snippets, shell commands, and optional single-file HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the bundled Python calculator; HTML reports may reference Chart.js from a CDN.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
