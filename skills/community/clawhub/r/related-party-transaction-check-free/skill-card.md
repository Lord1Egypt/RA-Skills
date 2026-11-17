## Description:

关联交易台账逐项核对，执行逐行复算、合计勾稽、重复与空缺检测，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and tax teams at companies with related-party transactions use this skill before annual tax filing and transfer-pricing documentation work to compare ledger amounts, transaction ledgers, report-form amounts, balances, pricing-method fields, duplicate rows, and missing required fields. It provides consistency checks only and does not provide legal, tax, valuation, or transfer-pricing opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive related-party transaction data beyond what is needed for the check.

Mitigation: Provide only the exported table text needed for the consistency checks and avoid unnecessary source-system or document content.

Risk: Consistency findings may be mistaken for legal, tax, or transfer-pricing advice.

Mitigation: Use the output as arithmetic and field-completeness review only, and route legal, tax, valuation, and transfer-pricing conclusions to qualified reviewers.

Risk: The free version intentionally omits several advanced checks.

Mitigation: Review the reported checks-not-run list before relying on the result, especially for materiality thresholds, long-term balances, and documentation-readiness questions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/related-party-transaction-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill definition](artifact/SKILL.md)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [CLI text or JSON findings with line numbers, severity levels, source evidence, summary counts, and scope details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; expects exported related-party transaction table text with recognizable headers.]

## Skill Version(s):

1.0.22 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
