## Description:

ShowMeTheMoney Lite guides users through a lightweight StablePay paid demo flow with wallet setup, visible pricing, and in-chat payment handling.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[bubblevan](https://clawhub.ai/user/bubblevan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to try a monetized StablePay workflow for a lightweight premium action, including free preview behavior and explicit payment confirmation before premium output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may initiate a real StablePay payment flow for the premium demo action.

Mitigation: Review the displayed price, currency, skill DID, and payment confirmation before approving payment.

Risk: Published merchant placeholders could make payment details ambiguous or unusable.

Mitigation: Confirm the published version uses real merchant values before installation or payment.

Risk: The skill is designed as a weak-protection paid demo and should not be treated as fully tamper-resistant.

Mitigation: Use it only for demos or lightweight premium actions and rely on StablePay confirmation before treating a purchase as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bubblevan/skills/showmethemoney-lite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown with structured payment setup steps, preview text, and payment status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide StablePay wallet setup and initiate payment only after an explicit paid demo request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
