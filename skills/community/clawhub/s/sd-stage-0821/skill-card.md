## Description:

Connects an agent to the Space Duck identity network for pairing, status checks, peer messaging, peck connections, Telegram binding, local listeners, and workspace-aware coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askegor](https://clawhub.ai/user/askegor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pair an agent with a Space Duck identity, manage trusted peer connections, send and receive pecks, run approved local listeners, and inspect network status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local listeners and local control paths can run on the operator's machine and may affect the agent environment.

Mitigation: Enable listener and owner-approval modes deliberately, use strict consent, and review each Telegram or Mission Control action before allowing command execution.

Risk: The skill relies on a Beak Key and optional Telegram credentials stored locally.

Mitigation: Keep local configuration files private, avoid exposing credentials in chat or command arguments, and rotate credentials if they may have been exposed.

Risk: Workspace bridge and synchronization features can expose or modify Markdown files in the configured workspace.

Mitigation: Scope workspace paths narrowly, avoid broad snapshots unless needed, and review bridge configuration before enabling synchronization.

Risk: Convenience approval modes such as Run all or 24-hour approvals can reduce per-action review.

Mitigation: Prefer one-action approvals and strict consent for normal use, especially when shell commands or updates are involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/askegor/skills/sd-stage-0821)
- [Publisher profile](https://clawhub.ai/user/askegor)
- [Space Duck API Reference](references/api.md)
- [Connection Ceremony](references/CONNECTION-CEREMONY.md)
- [Capability Grants](references/grants.md)
- [Space Duck MCP Client Spec](references/MCP-CLIENT-SPEC.md)
- [BYOB Workspace Bridge Reference Runtime](scripts/WORKSPACE_BRIDGE_README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and occasional JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide long-running listener setup, pairing flows, status checks, messaging workflows, and local configuration changes.]

## Skill Version(s):

0.8.21 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
