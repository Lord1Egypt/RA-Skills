## Description:

收支管理 is a Chinese-language local finance tracking skill for recording personal expenses, budgets, shop purchases and sales, inventory, and profit reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlrllr](https://clawhub.ai/user/wlrllr)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to track daily personal spending, monitor monthly budgets, record shop purchases and sales, check inventory, and generate monthly or annual finance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores finance records as local plaintext JSON files.

Mitigation: Keep the finance data directory out of shared folders, source control, and unencrypted backups, and consider tightening file permissions.

Risk: Profit, inventory, and budget reports may be estimates or may depend on the completeness of recorded transactions.

Mitigation: Verify calculations and source records before using reports for business, accounting, or tax decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlrllr/skills/wlrllr-finance-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/wlrllr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text finance reports with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores personal and shop finance records as local plaintext JSON files.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
