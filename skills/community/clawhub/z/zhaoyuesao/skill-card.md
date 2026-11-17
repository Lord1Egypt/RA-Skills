## Description:

找月嫂 helps users in supported Chinese cities request maternity matron services by collecting city, due-date timing, service period, budget, phone number, and SMS verification before submitting a lead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dj-skillhub](https://clawhub.ai/user/dj-skillhub)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request maternity matron service matching through a guided lead-submission workflow. The agent gathers service needs, confirms details, verifies the user's phone number by SMS, and submits the request to the service provider.

### Deployment Geography for Use:

China (supported cities)

## Known Risks and Mitigations:

Risk: The workflow handles sensitive phone and pregnancy-related information.

Mitigation: Use only after explicit user confirmation, mask phone numbers in user-facing output, and avoid environments where process logs are retained or shared.

Risk: The security summary identifies logging, endpoint-disclosure, and command-construction risks.

Mitigation: Review the skill before installation and deploy only where those risks are acceptable for a lead-generation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dj-skillhub/skills/zhaoyuesao)
- [Command reference](references/commands.md)
- [Error handling reference](references/errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Conversational text and markdown confirmations with shell command invocations and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before phone collection and masks phone numbers in user-facing output.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
