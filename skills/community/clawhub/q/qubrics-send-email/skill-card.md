## Description:

Send one or many emails through Qubrics using approved mailbox or agent credentials, idempotency keys, attachments, MCP, CLI, SDKs, or HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to prepare and send approved outbound email through Qubrics using MCP, CLI, SDK, or HTTP, including single messages, batches, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sending to the wrong account or recipients, or sending unapproved message content, can cause unintended disclosure or contact.

Mitigation: Verify the connection identity and mailbox, then get explicit approval of the complete sender, recipients, subject, body, and attachments before sending.

Risk: Email credentials can grant access to sending and may be exposed if shared in chat or placed in command arguments or output.

Mitigation: Load only the intended credential from a secret store; keep it out of chat, arguments, and output, and use an isolated process for CLI or SDK examples.

Risk: The security assessment is incomplete because some referenced material could not be resolved during scanning.

Mitigation: Review the referenced material and repeat the security scan when coverage gaps can be resolved.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-send-email)
- [Declared project homepage](https://github.com/qubrics/skills)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with JSON payloads, CLI commands, TypeScript examples, and HTTP requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes single-send and batch-send examples, credential setup guidance, attachment workflows, and response handling.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
