## Description:

把采购订单、入库单、发票放在一起核一遍，每条结论都带原文行号，不需要付款，也不需要注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounts payable users use this skill before payment to compare purchase order, goods receipt, and invoice text for matching order, supplier, item, quantity, unit price, amount, duplicate invoice-number, and placeholder issues. It is a local helper for limited document comparison, not a payment approval, fraud, invoice-authenticity, tax, tolerance, or compliance decision system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake a clean result for approval to pay or for proof that an invoice is authentic.

Mitigation: Use the output as a comparison aid only, and keep existing finance approval, invoice-authenticity, supplier, tax, and payment controls in place.

Risk: The free version intentionally omits arithmetic, tax, tolerance, date-sequence, and payment-term checks.

Mitigation: Confirm that the documented free-version checks are sufficient for the task before relying on the findings, and escalate documents that need omitted checks to a fuller review process.

Risk: Insufficient or poorly structured source documents can prevent meaningful comparison.

Mitigation: Provide at least two complete document texts with clear purchase order, goods receipt, or invoice fields; treat insufficient-input output as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/three-way-match-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Source skill definition](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [analysis, text, json, guidance]

**Output Format:** [Human-readable text or JSON findings with source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports insufficient input without drawing a consistency conclusion; findings are limited to the free-version checks documented by the skill.]

## Skill Version(s):

1.0.55 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
