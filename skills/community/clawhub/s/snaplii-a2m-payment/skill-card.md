## Description:

Agent-to-Merchant (A2M) payments — AI agents complete transactions without checkout, using Snaplii's pre-funded gift cards, accepted at over 500,000 locations, as a payment rail. Use when the user wants to browse, buy, or manage gift cards, check their Snaplii Cash balance, pay bills (utilities, telecom), or send money to another person's phone number (P2P transfer).

This skill is ready for commercial/non-commercial use.

## Publisher:

[snapliiai](https://clawhub.ai/user/snapliiai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to browse and manage Snaplii gift cards, check prepaid Snaplii Cash, and carry out requested gift-card purchases, bill payments, or person-to-person transfers through Snaplii.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested purchases and bill payments can execute without another confirmation; bill payments cannot be undone and are outside the gift-card daily limit.

Mitigation: Use only the needed permissions and conservative limits, and check the quote and biller or account details against the user's request before execution.

Risk: Transfers normally send automatically after about five minutes, and cross-currency transfers can deliver a different amount or currency.

Mitigation: Tell the user the amount, masked recipient, cancel deadline, and any cross-currency details; honor cancellation requests and only send immediately when explicitly asked.

Risk: The separately downloaded installer and payment runtime were unavailable for verification.

Mitigation: Follow the documented install and secure credential flows, grant only needed permissions, and revoke API keys in the Snaplii app when finished.

## Reference(s):

- [Snaplii AI Agent Cashback Payment on ClawHub](https://clawhub.ai/snapliiai/skills/snaplii-a2m-payment)
- [Snaplii app for iOS](https://apps.apple.com/app/snaplii/id1596924498)
- [Snaplii app for Android](https://play.google.com/store/apps/details?id=com.snaplii.app)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, API calls, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples and structured operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are host-specific and require an authenticated Snaplii session.]

## Skill Version(s):

1.14.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
