## Description:

Integrates OpenClaw agents with Signal messaging through signal-cli for sending and receiving text, attachments, voice messages, contact triage, conversation history, and wake-on-message notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucksus](https://clawhub.ai/user/lucksus)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect a standalone bot or account to Signal so an agent can receive messages, maintain conversation logs, triage unknown contacts, and send text or voice replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming Signal text may be written into agent-readable wake files before role-based controls are enforced in code.

Mitigation: Quarantine unknown or untrusted messages outside the agent context and require explicit owner approval before the agent reads or acts on them.

Risk: The bridge handles private Signal messages, contact identifiers, attachments, and conversation logs in local state files.

Mitigation: Use a dedicated low-privilege Signal account, restrict permissions on ~/.signal-state, and set retention limits for wake files, logs, and attachments.

Risk: The setup can install and invoke signal-cli and local wake/voice services as part of a messaging workflow.

Mitigation: Verify the signal-cli release before use, prefer user-local installation over sudo system-wide installation, and keep wake tokens and local service endpoints tightly scoped.

## Reference(s):

- [Signal Contact Permissions](references/permissions.md)
- [Troubleshooting](references/troubleshooting.md)
- [signal-cli](https://github.com/AsamK/signal-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational setup steps, messaging commands, contact permission guidance, and state file handling notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
