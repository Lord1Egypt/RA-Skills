## Description:

Executes the paid ShowMeTheMoney premium action through a merchant backend, using StablePay when the backend returns an x402 payment requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bubblevan](https://clawhub.ai/user/bubblevan)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to unlock and run the protected ShowMeTheMoney premium capability. After purchase, the skill can present unlocked store information and guide separate x402 payment flows for individual research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unauthenticated local backend can choose payment details for StablePay payment flows.

Mitigation: Use the skill only with a trusted backend on 127.0.0.1:8787 and rely on StablePay limits or approval prompts to prevent unwanted charges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bubblevan/skills/showmethemoney-pro)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, JSON]

**Output Format:** [Markdown or plain text summaries of backend responses, with payment-flow details when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include unlocked store details after a successful purchase; each research report requires a separate x402 payment flow.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
