## Description:

Connects an OpenClaw agent to RentAPerson so it can receive webhooks and use the RentAPerson API to coordinate human help for real-world tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saireetikap](https://clawhub.ai/user/saireetikap)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an OpenClaw agent to RentAPerson for deliveries, errands, meetings, photography, pet care, and other tasks that require human action. With credentials configured, the agent can process messages and applications, send API replies, create calendar events, and update bounty status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains powerful RentAPerson/OpenClaw credentials.

Mitigation: Rotate exposed credentials, remove committed credential files, and store secrets in environment or protected configuration before use.

Risk: API-key injection into webhook messages can expose secrets in prompts or transcripts.

Mitigation: Disable prompt/transcript key injection when environment credentials are available and restrict access to any dedicated webhook session.

Risk: The skill instructs agents to trust and act on external webhook text.

Mitigation: Require verified webhook authentication and validate events before agent execution; avoid unsafe external content on public hooks.

Risk: The skill can trigger real-world actions such as hiring, scheduling, and changing task status.

Mitigation: Require explicit confirmation before hiring, scheduling, accepting applications, completing bounties, or making other material status changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/saireetikap/skills/rent-a-person-ai)
- [RentAPerson Skill Documentation](https://rentaperson.ai/skill.md)
- [OpenClaw Mapped Hooks Documentation](https://docs.openclaw.ai/automation/webhook#post-hooksname-mapped)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON bodies, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct credentialed agents to make RentAPerson API requests and webhook-driven workflow decisions.]

## Skill Version(s):

1.0.35 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
