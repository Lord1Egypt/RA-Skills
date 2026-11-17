## Description:

Generates B2B customer success plans that connect customer goals to milestones, measurable outcomes, ownership, review cadence, and renewal signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External customer success teams, account managers, and implementation leads use this skill to turn customer goals, milestones, and resource constraints into review-ready success plans. The output is intended for planning, QBR preparation, and renewal-readiness review, not for promising services outside a contract or replacing formal project plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes local audit and pattern-scanning behavior beyond the described success-plan workflow.

Mitigation: Review the support script before installing and use the skill only for intended customer-success inputs.

Risk: Broad directory or repository inputs may expose more local file content than needed for a success plan.

Mitigation: Use specific input files, avoid sensitive repositories or broad directories, and prefer dry-run or stdout unless a local output file is required.

Risk: Customer-success materials may contain confidential customer or personal information.

Mitigation: Redact sensitive information before use and review generated drafts before sharing or acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/success-plan-generator)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Structured output specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown success-plan draft by default, with optional JSON report output from the support script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. The support script can print to stdout, run in dry-run mode, or write a local output file when explicitly requested.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
