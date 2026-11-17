## Description:

Analyze data with `pseudotime-trajectory-viz` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational biologists, and data analysts use this skill to run reproducible pseudotime trajectory analysis on preprocessed single-cell AnnData files and review trajectory plots, pseudotime values, lineage assignments, and analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted gene name can cause plot files to be written outside the chosen output folder.

Mitigation: Run the skill in an isolated workspace or container, use trusted .h5ad files, validate requested gene names, and review generated file paths before sharing results.

Risk: Trajectory results can be misleading when input data are low quality, batch affected, or interpreted as absolute time.

Mitigation: Validate trajectories with known marker genes and biological knowledge, compare methods for critical analyses, and document preprocessing assumptions.

## Reference(s):

- [Runtime Checklist](references/runtime_checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/pseudotime-trajectory-viz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; executed workflow writes plots, CSV, JSON, and AnnData files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a preprocessed AnnData (.h5ad) input; generated files are written to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
