## Description:

Helps users maintain an Excel expense ledger, reconcile edited workbooks and credit-card statements, and analyze spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuge897](https://clawhub.ai/user/jiuge897)

### License/Terms of Use:

MIT-0

## Use Case:

External users can maintain and review an Excel expense ledger through conversation, reconcile authorized workbook edits and credit-card statements, and analyze spending. The skill can return an updated workbook and summaries or charts while preserving the existing ledger structure where possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ledger files contain personal financial data, and proposed workbook changes may be incorrect or conflict with newer edits.

Mitigation: Limit access to the intended ledger and statements, review reported changes and conflicts, and keep recoverable versions before confirming updates.

## Reference(s):

- [Ledger Contract](references/ledger-contract.md)
- [ClawHub Skill Release](https://clawhub.ai/jiuge897/skills/reconcile-expense-ledger)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [Updated Excel workbooks, reconciliation summaries, and spending analyses with charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves workbook structure where possible; keeps currencies separate unless conversion is requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
