## Description:

Manage VMware NSX networking, including segments, gateways, NAT, routing, IP pools, fabric inventory, health checks, and connectivity troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers and developers use this skill to inspect and manage VMware NSX segments, gateways, NAT, routes, and IP pools, and to diagnose NSX health and connectivity issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses NSX credentials and stores audit or policy data locally.

Mitigation: Protect credential and audit files with restrictive permissions or a secret manager, and retain authentication checks.

Risk: Write actions can change NSX network configuration, and optional HTTPS transport opens a listener.

Mitigation: Keep local stdio as the default, require an explicit request for each write, review dry-run previews, and authenticate any HTTPS listener.

Risk: Security guidance reports an unpinned Docker image reference and incomplete scan coverage for one unresolved path-like reference.

Mitigation: Verify the Docker image identity and review the unresolved reference before relying on the scan results.

## Reference(s):

- [Project repository](https://github.com/vmware-skills/VMware-NSX)
- [Capabilities](artifact/references/capabilities.md)
- [Setup guide](artifact/references/setup-guide.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration]

**Output Format:** [Structured MCP responses, diagnostic text, Markdown guidance, shell commands, and configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations target the configured NSX Manager; write actions require an explicit request.]

## Skill Version(s):

1.15.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
