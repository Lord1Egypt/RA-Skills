## Description:

Helps users select and manage Fengniao cloud numbers and physical SIM cards through Qinghu, including orders, SMS retrieval, renewals, and account transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users managing cross-border commerce accounts can compare phone-number products, check SMS and account status, and request purchases, renewals, returns, recharges, or withdrawals with explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Purchases, payments, recharges, withdrawals, renewals, returns, and number changes can affect real funds or active phone numbers.

Mitigation: Review the account, amount, target numbers, and effects; require explicit confirmation before each action and verify its status before reporting completion.

Risk: Qinghu API tokens and SMS messages may expose sensitive account or verification information.

Mitigation: Provide the token only when needed, protect it from disclosure, and share only the SMS content the user specifically requests.

Risk: Broad phone-number or SMS-registration requests may activate this skill unintentionally.

Mitigation: Confirm the user intends to use Qinghu/Fengniao services before authorizing tools; decline unintended tool requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-fengniao-cloud-number)
- [Fengniao cloud-number service](https://fnyunhao.com/)
- [Qinghu API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown responses with product details, account status, SMS summaries, and transaction confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide a payment QR-code image for user-initiated recharge.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
