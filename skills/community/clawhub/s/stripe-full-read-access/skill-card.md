## Description: <br>
Access Stripe directly with a Stripe secret or restricted API key for broad read-only platform queries, especially Connect accounts, application fees, balances, charges, customers, invoices, subscriptions, payouts, transfers, and balance transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgelewi5](https://clawhub.ai/user/georgelewi5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and finance analysts use this skill to query Stripe platform and Connect data directly for read-oriented reporting, reconciliation, and account analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence says the skill is framed as read-only but appears capable of account-changing Stripe actions when asked. <br>
Mitigation: Use a narrowly scoped read-only Stripe restricted key when possible, avoid full secret keys unless financial changes are intended, and require explicit confirmation before any refund, payout, transfer, subscription, customer, or account mutation. <br>
Risk: The skill depends on a locally stored Stripe API key. <br>
Mitigation: Keep Stripe keys outside git, do not write keys into memory files, and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/georgelewi5/stripe-full-read-access) <br>
- [Stripe API base URL](https://api.stripe.com/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Stripe API endpoint paths, pagination guidance, and read-only reporting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
