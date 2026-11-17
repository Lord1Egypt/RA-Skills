## Description:

Manage Tailscale tailnet operations through local Tailscale CLI commands and tailnet-wide API helper commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmagar](https://clawhub.ai/user/jmagar)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and Tailscale administrators use this skill to inspect tailnet status, test connectivity, transfer files, expose services, and manage devices, auth keys, DNS, and ACL validation from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform powerful tailnet administration actions, including deleting devices or auth keys and changing device, DNS, or ACL-related settings.

Mitigation: Review write and delete commands before execution, and manually verify device IDs, key IDs, tags, ports, and target tailnet details.

Risk: API access requires a Tailscale API key that could administer tailnet-wide resources if over-scoped or exposed.

Mitigation: Use a narrowly scoped, short-lived API key where possible, store credentials with restrictive permissions, and avoid printing or sharing secrets.

Risk: Tailscale Funnel commands can expose a local service to the public internet.

Mitigation: Confirm that public exposure is intended, verify the service and port, and disable Funnel when public access is no longer needed.

## Reference(s):

- [ClawHub Tailscale Skill](https://clawhub.ai/jmagar/skills/tailscale)
- [Tailscale Admin Console API Keys](https://login.tailscale.com/admin/settings/keys)
- [Tailscale Download](https://tailscale.com/download)
- [Tailscale API v2 Endpoint](https://api.tailscale.com/api/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tailscale CLI commands and API helper commands whose API responses are JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
