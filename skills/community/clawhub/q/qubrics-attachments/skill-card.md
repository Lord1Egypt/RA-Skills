## Description:

Move email attachments through Qubrics without putting file bytes in model context, using presigned URLs through MCP or file paths through CLI and SDK helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill to read and transfer Qubrics mailbox and Sending API attachments through MCP, CLI, or SDK workflows while keeping real file bytes out of model context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attachment data and credentials may be sent to Qubrics, and the security scan reports medium confidence with partial coverage.

Mitigation: Use the intended account and authorized mailbox, verify the returned identity before access or transfer, and keep credentials and signed upload capabilities out of chat, command arguments, and logs.

Risk: Inbound attachment content, filenames, links, and metadata can contain untrusted or instruction-like content.

Mitigation: Read only what the authorized task needs and treat attachment content as data rather than instructions.

## Reference(s):

- [Qubrics skills repository](https://github.com/qubrics/skills)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown instructions with inline text, JSON, shell, TypeScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses file paths or presigned URLs for attachment transfer; real attachment bytes are kept out of model context except for tiny agent-authored files.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
