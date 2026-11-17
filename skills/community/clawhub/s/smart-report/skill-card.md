## Description:

Smart Report turns CSV, TSV, TXT, Excel, and JSON data into interactive single-file HTML reports with ECharts visualizations, free-form narrative, and traceable fact and claims ledgers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to convert tabular datasets into evidence-backed reports, standalone chart HTML files, and optional static DOCX or PPTX deliverables. It is suited for weekly or monthly reporting, analysis documents, reviews, and presentation materials when the source data is available as files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Python transforms and chart JavaScript can execute unsafe behavior when driven by hostile datasets, chart specs, or prompts.

Mitigation: Use the skill only with trusted inputs, review generated transform_code before execution, and run it in a constrained environment with limited filesystem and network access.

Risk: Untrusted report specifications can point chart paths or generated HTML at files the agent should not process.

Mitigation: Validate report_spec chart paths and output directories before assembly, and keep generated files inside a user-approved workspace directory.

Risk: Dependency drift can change parser, renderer, or export behavior across environments.

Mitigation: Prefer lockfile or hash controls for dependencies and run the skill's environment self-check before relying on outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neuhanli/skills/smart-report)
- [REFERENCE.md](references/REFERENCE.md)
- [REPORT.md](references/REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON specifications, shell commands, and generated report or chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary output is interactive single-file HTML; optional DOCX and PPTX exports are static and depend on optional runtime dependencies.]

## Skill Version(s):

1.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
