## Description:

Choose low-token Qubrics calls across MCP, CLI, SDKs, and HTTP by using snippets, counts, batches, deltas, cursors, ETags, and idempotency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose efficient Qubrics mailbox, sending, and management calls across MCP, CLI, SDK, and HTTP. It guides credential and account checks, narrower reads, batching, and safe retries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes possible agent setup and owner-management actions, while purpose alignment remains uncertain.

Mitigation: Review whether setup, mailbox access, and owner invitations fit the intended use; verify the connection identity and approved mailbox before task work, and stop if identity cannot be confirmed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-token-efficient-usage)
- [Qubrics skills project](https://github.com/qubrics/skills)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Code]

**Output Format:** [Markdown guidance with CLI examples and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends bounded reads, batching, delta sync, conditional requests, and idempotent retries.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
