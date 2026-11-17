## Description:

SPSS Data Cleaning Assistant helps users diagnose and clean SPSS, CSV, Excel, and TSV datasets by identifying missing values, outliers, type issues, duplicate records, recoding needs, and validation problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zihaowyt5525-max](https://clawhub.ai/user/zihaowyt5525-max)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and agents working with survey, experiment, public-opinion, or similar research datasets use this skill to plan, execute, validate, and document data-cleaning steps before analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded datasets may contain personal, regulated, confidential, or proprietary information.

Mitigation: Use only authorized datasets, remove identifying fields where appropriate, and avoid uploading sensitive data unless permitted.

Risk: Cleaning actions such as deletion, recoding, imputation, or outlier handling can change analysis results.

Mitigation: Run cleaning on a copy of the original dataset, review the proposed plan before approving changes, and keep the generated cleaning log.

Risk: Unpinned data-processing dependencies can create reproducibility or environment risk.

Mitigation: Install dependencies in an isolated environment and prefer pinned package versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zihaowyt5525-max/skills/spss-data-cleaning)
- [Skill artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, code snippets, shell commands, and generated data-cleaning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cleaned dataset exports in SPSS .sav and CSV formats when the agent has access to the necessary workspace files and dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
