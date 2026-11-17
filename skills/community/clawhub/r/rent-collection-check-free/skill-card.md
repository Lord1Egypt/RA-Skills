## Description:

租金收缴与欠租台账核对（免费版）核对租金收缴与欠租台账的逐行算术、合计勾稽、重复与空缺，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, property, and asset-management users use this skill during monthly closing, reconciliation, and ledger review to check rent collection and arrears tables before relying on them for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat table arithmetic and consistency findings as accounting, tax, legal, or contract advice.

Mitigation: Use the output as reconciliation assistance only and have qualified reviewers handle accounting, tax, legal, and contract judgments.

Risk: The free version explicitly omits several advanced rent-ledger checks.

Mitigation: Review the listed withheld checks and do not interpret omitted findings as evidence that those issues were checked.

Risk: Incomplete or unrecognized input can otherwise lead users to over-read the absence of findings.

Mitigation: Treat insufficient-input responses as non-conclusions and provide a table with the required headers and rows before using the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/rent-collection-check-free)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON result reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing requirements rather than a positive conclusion.]

## Skill Version(s):

1.0.46 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
