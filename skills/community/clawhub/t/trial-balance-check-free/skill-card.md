## Description:

A free deterministic checker for Chinese-style trial balance sheets that recomputes closing balances, checks profit-and-loss account closeout, verifies debit and credit totals, checks parent and child account subtotals, and flags duplicate, blank, or non-numeric entries with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting staff, finance managers, and auditors use this skill during monthly closing or pre-audit review to check whether a pasted account balance table is internally balanced and whether required period-end closeout conditions hold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accounting records can contain sensitive financial information.

Mitigation: Review input data for sensitivity before providing it to the local checker and avoid sharing unnecessary records.

Risk: Incorrect table headers, balance signs, or pre-close amounts can lead to incomplete or misleading results.

Mitigation: Use the documented input columns and sign convention, and review missing-input messages before relying on findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/trial-balance-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON containing trial-balance findings, missing-input guidance, executed checks, withheld checks, and source line references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js and does not require network access or API keys.]

## Skill Version(s):

1.0.52 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
