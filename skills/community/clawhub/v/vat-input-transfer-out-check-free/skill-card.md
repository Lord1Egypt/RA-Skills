## Description:

进项税额转出计算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during monthly close, reconciliation, or review to check input VAT transfer-out calculation tables for arithmetic mismatches, totals issues, duplicate rows, blanks, and negative amounts. It reports findings with source-line evidence and withholds conclusions when required table material is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat table-consistency findings as legal or tax advice.

Mitigation: Use the skill as an arithmetic and consistency checker only; consult qualified tax guidance for VAT treatment decisions.

Risk: The free edition explicitly omits several higher-tier checks.

Mitigation: Review the omitted checks before relying on a clean result, and do not treat the free-edition output as a complete VAT compliance review.

Risk: The skill runs a local Node.js script against VAT transfer-out table text.

Mitigation: Run it only in a trusted local workspace and review the provided files before execution; server security evidence reports no network use, persistence, credential access, or hidden high-impact behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/vat-input-transfer-out-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console text or JSON result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js against user-provided VAT table text; sample input is provided as JSON.]

## Skill Version(s):

1.0.54 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
