## Description:

Analyze data with `survival-curve-risk-table` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and clinical research teams use this skill to generate aligned number-at-risk tables for Kaplan-Meier survival curves and export review-ready survival-chart artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags pickle dataset support as review-worthy because opening .pkl or .pickle files can be unsafe when files are untrusted.

Mitigation: Use trusted CSV, Excel, or SAS inputs by default, and only open pickle datasets from trusted sources in an isolated environment.

Risk: The security review flags ambiguous unpinned dependencies, including an ambiguous pil dependency.

Mitigation: Install in an isolated virtual environment, pin reviewed package versions, and remove the pil dependency before broad use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/aipoch-ai/skills/survival-curve-risk-table)
- [Runtime Checklist](artifact/references/runtime_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with CLI and Python examples; generated chart files may include PNG, PDF, SVG, and PowerPoint-compatible outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires validated survival data columns and local Python dependencies before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
