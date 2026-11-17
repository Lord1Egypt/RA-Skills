## Description:

Skill Quality Evaluator - Score any skill on 6 dimensions. Catch 30% of skills that look good but fail silently. Based on Tessl Research 2026 findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to evaluate agent skills across activation reliability, task coverage, instruction clarity, leakage resistance, model compatibility, and real-world value. It helps produce concise quality reports with critical issues, recommendations, and quick wins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation reports can capture private or proprietary details from the skills being reviewed when batch mode or memory output is used.

Mitigation: Confirm that storing or sharing evaluation reports is acceptable before retaining outputs, especially for internal or proprietary skills.

Risk: The skill provides a structured quality assessment, but its scores may not substitute for task-specific testing of the evaluated skill.

Mitigation: Use the report as review guidance and pair it with representative evaluation tasks before relying on score thresholds for release decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evaluation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include numeric scores, status indicators, critical issues, recommendations, and quick wins.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
