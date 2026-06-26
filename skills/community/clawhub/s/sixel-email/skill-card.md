## Description: <br>
1:1 email channel for agents — the agent can only email one address, and only that address can email the agent. Also handles the heartbeat (poll to prove you're alive). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sixel-et](https://clawhub.ai/user/sixel-et) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to send email updates, ask for asynchronous operator input, receive replies, and maintain a heartbeat through the sixel.email service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a SIXEL_API_TOKEN credential for sending and polling email. <br>
Mitigation: Confirm the token is scoped only to the intended agent/operator channel and keep it out of email bodies, logs, and shared output. <br>
Risk: Email bodies and attachments can carry secrets, misleading instructions, or untrusted files. <br>
Mitigation: Do not send secrets over plaintext email, treat inbound messages and attachments as untrusted, and download attachments only into a dedicated directory with agent-generated filenames. <br>
Risk: Background polling may run continuously and handle inbound data outside the agent's main flow. <br>
Mitigation: Run any background poller in a constrained environment and process unread messages before polling again because inbox polling marks messages as read. <br>


## Reference(s): <br>
- [sixel.email homepage](https://sixel.email) <br>
- [sixel.email best practices](https://sixel.email/best-practices) <br>
- [ClawHub skill listing](https://clawhub.ai/sixel-et/sixel-email) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides instructions for authenticated sixel.email API calls, attachment handling, inbox polling, and operational safety practices.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
