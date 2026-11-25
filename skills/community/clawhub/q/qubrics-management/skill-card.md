## Description:

Manage Qubrics domains, mailboxes, mailbox keys, sending accounts, webhooks, logs, billing, and account-level setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team administrators use this skill to manage Qubrics domains, mailboxes, sending accounts, webhooks, billing, and delivery logs through CLI, SDK, HTTP, and MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because some local path-like references could not be resolved; a benign verdict does not guarantee no risk.

Mitigation: Review the skill and its installation mechanism, including unresolved references, before installing.

Risk: Management workflows can use sensitive credentials and perform destructive account changes.

Mitigation: Keep credentials out of chat and command output, load them from the chosen secret store, and confirm the target before destructive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roshanjonah/skills/qubrics-management)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API calls]

**Output Format:** [Markdown with CLI examples, JSON request bodies, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.8 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
