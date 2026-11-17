## Description:

Sign up for and log into services using your Ravi identity, including onboarding, forms, 2FA, OTPs, and credential storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Ravi authentication, identity selection or creation, website signup, login, credential retrieval, and OTP or email verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and retrieve website credentials and use stored Ravi authentication material.

Mitigation: Use only on a trusted machine and review credential-related commands before execution.

Risk: The skill can inspect Ravi SMS and email inbox content for verification codes or links.

Mitigation: Limit use to signup and login verification workflows, and use dedicated Ravi inbox or email skills for standalone inbox reading or email sending.

## Reference(s):

- [Ravi Login Skill on ClawHub](https://clawhub.ai/raunaksingwi/skills/ravi-login)
- [Ravi Device Auth Schema](https://ravi.id/docs/schema/device-auth.json)
- [Ravi Auth and Keys Schema](https://ravi.id/docs/schema/auth.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include Ravi CLI commands, form-filling values, credential lookup steps, and OTP or verification-link extraction steps.]

## Skill Version(s):

2.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
