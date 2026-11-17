## Description:

Professional home inspection for Taiwan residential properties using structured checklists, defect severity grading, Taiwan building-standard references, and Markdown report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and property professionals use this skill to plan Taiwan residential inspections, record findings, classify defects by severity, and generate formal Markdown inspection reports. It is a guide and reporting tool; final decisions for structural concerns should remain with licensed professionals.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: The skill instructs the agent to run `skills/analytics.py`, but that script is not included in the reviewed artifact.

Mitigation: Do not run `skills/analytics.py` unless the installed script is separately verified.

Risk: The report generator writes to a caller-provided output path.

Mitigation: Direct report output to a specific safe `.md` path and avoid paths that could overwrite important files.

Risk: Inspection guidance may involve structural or safety-critical decisions.

Mitigation: Use generated findings as documentation support and refer structural concerns to qualified professionals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/taiwan-home-inspection)
- [Inspection Checkpoints](references/checkpoints.md)
- [Defect Severity Criteria](references/defects.md)
- [Taiwan Building Standards Reference](references/standards.md)
- [Report Template](assets/report-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown reports and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 for report generation from an input JSON file to a caller-selected Markdown output path.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
