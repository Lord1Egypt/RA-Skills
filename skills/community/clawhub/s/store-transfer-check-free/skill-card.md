## Description:

门店调拨与库存核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and store operations staff use this skill during monthly closing, reconciliation, or stocktaking to check chain-store transfer and inventory tables. It recalculates row arithmetic, total rows, duplicate document numbers, blanks, and selected negative quantities, while citing source rows and declining to conclude when input is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes store transfer and inventory table data through a local Node.js script.

Mitigation: Run it only in an environment approved for that operational data and review the local script before deployment.

Risk: The skill is a reconciliation aid, not a full audit, ERP/WMS connector, approval-control check, or physical inventory substitute.

Mitigation: Use the findings as row-level checks and confirm material decisions through the normal inventory, approval, and audit processes.

Risk: The free edition intentionally omits several checks, including negative in-transit or ending stock checks and some transfer-variance checks.

Mitigation: Review the reported checks_not_run or withheld-check list before relying on a result as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/store-transfer-check-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown instructions and local command output; optional JSON result output from the bundled Node.js runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; local execution reports which checks ran, which checks were withheld, and whether input was insufficient.]

## Skill Version(s):

1.0.52 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
