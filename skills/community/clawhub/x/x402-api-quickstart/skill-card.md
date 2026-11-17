## Description:

Guides agents through calling x402 pay-per-call APIs using USDC payments on Base and provides six example endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to understand the HTTP 402 payment flow and test pay-per-call APIs with example endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent with access to a funded Base wallet could incur charges when following paid API guidance without spending limits or confirmation rules.

Mitigation: Use only known x402 endpoints, set per-call and session spending caps, and require explicit approval for a new host or amounts outside the listed examples.

## Reference(s):

- [Published x402 API Quickstart skill](https://clawhub.ai/perria080925-bot/skills/x402-api-quickstart)
- [One Dollar Quest public worklog (linked in the skill)](https://github.com/perria080925-bot/one-dollar-quest)
- [Example x402 endpoints](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an HTTP 402 payment flow and six priced example endpoints.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
