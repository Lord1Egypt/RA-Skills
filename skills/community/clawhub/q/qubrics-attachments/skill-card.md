## Description:

Move email attachments through Qubrics without putting file bytes in model context, using presigned URLs through MCP or file paths through CLI and SDK helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read, upload, and send email attachments through Qubrics MCP, CLI, SDK, or HTTP workflows while keeping file bytes out of model context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attachment workflows may transmit files to Qubrics and use optional API credentials.

Mitigation: Use an authorized Qubrics account and mailbox, verify the returned identity, and load credentials from a secret store rather than chat.

## Reference(s):

- [Project homepage](https://github.com/qubrics/skills)
- [ClawHub release](https://clawhub.ai/roshanjonah/skills/qubrics-attachments)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API request examples, Configuration instructions]

**Output Format:** [Markdown with inline shell, TypeScript, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides attachment workflow instructions and examples; does not place real file bytes in model context.]

## Skill Version(s):

2.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
