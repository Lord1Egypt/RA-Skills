## Description:

Set up Qubrics for agents, register a durable inbox without an existing key, link an owner, choose a runtime surface, and make the first harmless call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure Qubrics access, register or link an agent inbox, choose the appropriate API surface, and verify a first harmless call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious (Review), citing a mismatch between its onboarding purpose and management access and an install command that is not pinned. The scan was partial because it could not resolve several references.

Mitigation: Review the reported mismatch and confirm the intended install source and release before installing, as the skill advises.

Risk: An inherited credential or incorrectly selected profile could connect an agent to an unintended Qubrics identity.

Mitigation: Clear inherited credential overrides in an isolated process, select the intended profile or secret, and verify the returned identity before mailbox access or sending.

## Reference(s):

- [Qubrics skills repository](https://github.com/qubrics/skills)
- [Qubrics hosted MCP endpoint](https://mcp.qubrics.com/mcp)
- [ClawHub release](https://clawhub.ai/roshanjonah/skills/qubrics-getting-started)
- [Qubrics Sending connection endpoint](https://smtp.qubrics.com/api/v1/me)
- [Qubrics Mailbox connection endpoint](https://app.qubrics.com/api/v1/mailbox/connection)
- [Qubrics Management connection endpoint](https://app.qubrics.com/api/v1/me)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, API calls]

**Output Format:** [Markdown guidance with CLI, HTTP, MCP, and SDK examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential handling and connection verification instructions.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
