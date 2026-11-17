## Description:

End-to-end Agent-to-Merchant autopilot: buy a Snaplii gift card with cashback, then drive the browser to redeem it on the merchant/delivery site and place the order — all in one flow. Use when the user wants the agent to actually complete a purchase or food/delivery order (e.g. 'order me a coffee on Uber Eats and pay with Snaplii'), not just get a gift card. Requires a browser-automation tool in the session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snapliiai](https://clawhub.ai/user/snapliiai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the agent to complete a merchant or food delivery purchase with Snaplii: select and buy a gift card, redeem it on the merchant site, and place the order after the required approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A gift card is charged before merchant checkout, so a failed or declined order can leave the purchased card in the user's Snaplii account.

Mitigation: Show the full gift-card quote and explain the charge timing and retained-card outcome; wait for explicit approval before buying.

Risk: Submitting the merchant order creates a separate financial commitment.

Mitigation: Show the items, delivery address, tip, and total, then wait for the user's explicit current-turn approval before placing the order.

Risk: Credentials could be exposed if entered through an ordinary chat or command argument.

Mitigation: Enter keys only in the prescribed secure credential dialog or hidden terminal prompt.

Risk: The external installer and runtime were unavailable for verification, so the security verdict covers the bundled instructions only.

Mitigation: Verify the installation source and runtime before connecting an account or authorizing payments.

## Reference(s):

- [Snaplii Autopilot release on ClawHub](https://clawhub.ai/snapliiai/skills/snaplii-autopilot)
- [Snaplii agent-to-merchant installation repository](https://github.com/Snaplii-Inc/agent-to-merchant-payments.git)
- [Snaplii payment service](https://aipayment.snaplii.com)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls, Browser actions]

**Output Format:** [Natural-language guidance and user-facing confirmations with structured tool and browser actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Snaplii runtime and browser automation; purchases and final order placement require explicit user approval.]

## Skill Version(s):

1.6.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
