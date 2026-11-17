## Description:

Assess translational gaps between preclinical models and human diseases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and developers use this skill to generate structured translational-gap assessments for preclinical models, diseases, model comparisons, and focused biological domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation instructions include unpinned requirements, which can introduce avoidable supply-chain risk.

Mitigation: Install and run the skill only in an isolated environment, and avoid dependency installation unless the requirements are removed, pinned, or reviewed.

Risk: The script can write reports to a user-supplied output path without enforcing a workspace boundary.

Mitigation: Use --output only with a clearly workspace-local new file path and review the target path before execution.

Risk: The skill produces scientific risk guidance that may affect research decisions if treated as authoritative.

Mitigation: Treat generated assessments as decision-support summaries and require domain expert review before relying on results.

## Reference(s):

- [Audit Reference](references/audit-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, JSON, or plain-text table report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include model and disease inputs, gap scores, risk levels, dimension concerns, clinical failure predictors, and recommendations; output may be printed or written to a user-specified file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
