## Description:

该技能本地核对 SaaS 订阅收入确认表的逐行复算、合计勾稽、重复与空缺问题，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting staff use this skill during monthly close, reconciliation, or review to check SaaS subscription revenue recognition tables for arithmetic, roll-forward, duplicate-row, blank-field, and negative-amount issues. The skill is a local checker and does not replace accounting judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free edition omits several checks that a full revenue recognition review may need.

Mitigation: Use the disclosed executed and withheld check lists when interpreting results, and do not treat omitted checks as completed.

Risk: The checker validates table mechanics but does not decide the correct accounting treatment for a subscription.

Mitigation: Have qualified accounting staff review recognition timing, allocation policy, contract changes, tax, currency, and other judgment-based matters.

Risk: Insufficient or malformed input can prevent reliable findings.

Mitigation: Provide the SaaS revenue recognition table with headers and review missing-input messages before relying on output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/saas-revenue-recognition-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Console text or JSON findings that an agent can summarize in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing requirements instead of a clean-result conclusion.]

## Skill Version(s):

1.0.46 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
