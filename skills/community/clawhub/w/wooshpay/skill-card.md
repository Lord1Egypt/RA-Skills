## Description:

WooshPay Payment Gateway Integration for creating payments, checking order status, processing refunds, and managing checkout sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wp-ai-dev](https://clawhub.ai/user/wp-ai-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and merchants use this skill to run interactive WooshPay payment, checkout, order-status, and refund workflows from an agent-assisted terminal session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merchant API keys or payment client secrets may be exposed in chat logs or terminal output.

Mitigation: Use a restricted WooshPay key where possible, keep the key in WOOSHPAY_API_KEY, do not paste API keys into chat, and redact client secrets from shared logs.

Risk: Order-status lookup can send the Authorization header to a user-supplied full URL.

Mitigation: Use only WooshPay payment intent IDs such as pi_... for status checks and avoid running get_payment.py with any full URL.

Risk: Payment and refund commands can affect live merchant transactions.

Mitigation: Confirm amounts, currencies, payment intent IDs, and refund eligibility in WooshPay before approving interactive prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wp-ai-dev/skills/wooshpay)
- [WooshPay getting started](https://docs.wooshpay.com/3647644m0)
- [WooshPay payment methods](https://docs.wooshpay.com/3948703m0)
- [WooshPay supported currencies](https://docs.wooshpay.com/2447438m0)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Terminal text with JSON API responses, status details, and generated payment or checkout URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WOOSHPAY_API_KEY. The packaged artifact contains create, checkout, status, and refund scripts; the documented cancel script is not present.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
