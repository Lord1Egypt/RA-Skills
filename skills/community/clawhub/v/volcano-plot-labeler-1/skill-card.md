## Description:

Analyze data with `volcano-plot-labeler` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to label the most significant genes in volcano plots from differential expression CSV or TSV data. It helps produce review-ready plots with ranked gene labels, threshold styling, and explicit assumptions about inputs and outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local CSV or TSV data and writes plot files, so broad filesystem access can expose unintended inputs or outputs.

Mitigation: Run it in an isolated workspace and provide only the intended input and output paths.

Risk: Unpinned Python dependencies can change runtime behavior across environments.

Mitigation: Use an isolated Python environment and pin or lock dependency versions before production use.

Risk: The checklist names path-validation and workspace-restriction controls that are not proven implemented safeguards.

Mitigation: Enforce path restrictions in the calling environment rather than relying on checklist text alone.

## Reference(s):

- [Volcano Plot Labeler on ClawHub](https://clawhub.ai/aipoch-ai/skills/volcano-plot-labeler-1)
- [Runtime Checklist](references/runtime_checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local volcano plot image files such as PNG, PDF, or SVG when run with valid CSV or TSV input.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
