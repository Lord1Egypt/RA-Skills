## Description: <br>
Manage Razorpay customers, orders, invoices, payment links, refunds, payouts, and payment operations via the Razorpay API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and manage Razorpay payments, customers, orders, invoices, payment links, refunds, payouts, contacts, fund accounts, items, settlements, and disputes from an agent workflow. It is intended for account-connected payment operations where write actions are confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment, refund, payout, invoice, and payment-link operations can affect real money or customer-facing payment state. <br>
Mitigation: Confirm the target resource, amount, customer details, and intended effect before any write action, and preview supported write actions before execution. <br>
Risk: The skill requires an OAuth-connected Razorpay account and sensitive payment access through ClawLink. <br>
Mitigation: Use the hosted ClawLink connection flow, avoid placing API keys in chat, verify the active Razorpay connection before tool use, and keep access scoped to the connected account. <br>
Risk: Tool availability and parameters may change in the live ClawLink catalog. <br>
Mitigation: List or search the live Razorpay tools and describe unfamiliar tools before calling them instead of guessing tool names or schemas. <br>


## Reference(s): <br>
- [Razorpay API Documentation](https://razorpay.com/docs/api/) <br>
- [Razorpay Orders API](https://razorpay.com/docs/api/payments/orders/) <br>
- [Razorpay Invoices API](https://razorpay.com/docs/api/invoices/) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/razorpay-payments) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Razorpay resource identifiers, amounts in paise, connection checks, previews, and confirmation prompts for write operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
