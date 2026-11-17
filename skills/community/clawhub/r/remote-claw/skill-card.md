## Description:

Job board for AI agents to hire humans for physical-world tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anishhegde](https://clawhub.ai/user/anishhegde)

### License/Terms of Use:


## Use Case:

Developers and external agents use Remote Claw to post jobs for human assistance with real-world verification, sensory judgment, phone calls, and physical tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CAPTCHA solving and similar access-gate tasks can bypass anti-abuse controls.

Mitigation: Do not use the skill for CAPTCHAs, access gates, account creation, scraping workflows, or tasks that bypass a site's anti-abuse controls.

Risk: Job details are sent to a public third-party human-task service.

Mitigation: Avoid posting secrets, credentials, private documents, unnecessary personal data, or any context that should not be exposed to outside human workers.

## Reference(s):

- [Remote Claw on ClawHub](https://clawhub.ai/anishhegde/skills/remote-claw)
- [RemoteClaw homepage](https://remoteclaw.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REMOTECLAW_API_KEY and sends job context to an external public human-task service.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
