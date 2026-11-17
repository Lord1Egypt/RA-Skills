## Description:

Ravi helps agents use Ravi-provided identity services, including email, phone, inbox, contacts, passwords, and encrypted secret storage for agent identity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to route agents toward Ravi identity, inbox, email, login, password, secret, SSO, and contact workflows. It is intended for tasks involving agent identity, email, phone, or credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to send feedback email after Ravi workflows, which could disclose sensitive account, OTP, inbox, password, secret, contact, or SSO details.

Mitigation: Require explicit user approval for the exact feedback message and redact sensitive details before sending any feedback email.

Risk: Ravi workflows can involve plaintext credentials, secrets, inbox contents, and phone or email identity data.

Mitigation: Limit use to user-approved identity, email, phone, and credential tasks, and avoid exposing plaintext secrets or message contents unless needed for the requested workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raunaksingwi/skills/ravi)
- [Publisher profile](https://clawhub.ai/user/raunaksingwi)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes routing guidance for Ravi-related identity, inbox, email, login, password, secret, SSO, contact, and feedback workflows.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
