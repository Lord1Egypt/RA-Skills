## Description:

Manage Qubrics domains, mailboxes, mailbox keys, sending accounts, webhooks, logs, billing, and account-level setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Qubrics team administrators use this skill to manage domains, mailboxes, sending accounts, webhooks, billing, and delivery records. It provides operational guidance and examples for choosing a management surface and handling permissions and credentials safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Management workflows may expose account credentials or sensitive one-time API key and webhook-secret values.

Mitigation: Load only the intended credential from the user's secret store, keep credentials out of chat, command arguments, and output, and place one-time values only in the chosen secret store or secure output path.

Risk: Administrative changes can affect domains, mailboxes, keys, sending accounts, or webhooks.

Mitigation: Verify the selected connection identity and effective permissions, confirm the target resource, and obtain confirmation before destructive operations.

Risk: The security assessment was partial because some references could not be resolved.

Mitigation: Review the skill's unresolved references and assess the related resources before relying on the skill.

## Reference(s):

- [Project homepage (listed in skill metadata)](https://github.com/qubrics/skills)
- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-management)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions, API calls]

**Output Format:** [Markdown with shell, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover MCP, CLI, SDK, and HTTP management workflows.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
