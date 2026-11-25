## Description:

Manage VMware NSX/NSX-T networking, including segments, gateways, NAT, routing, IP pools, fabric inventory, health checks, and connectivity diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators and infrastructure engineers use this skill to inspect NSX environments, diagnose health and connectivity issues, and manage network configuration when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was benign with medium confidence, but scan coverage was partial and the setup guide was partly inspected.

Mitigation: Review the setup guide before installation, especially credential configuration and the authentication-skip option.

Risk: Write operations can change NSX network configuration.

Mitigation: Only make explicitly requested changes, and review dry-run output or delete previews before confirming an operation.

## Reference(s):

- [Setup guide](references/setup-guide.md)
- [Capabilities](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Agent guardrails](references/agent-guardrails.md)
- [Detailed guide](references/detailed-guide.md)
- [Project homepage](https://github.com/vmware-skills/VMware-NSX)
- [ClawHub release](https://clawhub.ai/zw008/skills/vmware-nsx)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [Concise text or Markdown, structured JSON results, and CLI or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic summaries and proposed network changes; write actions require an explicit user request.]

## Skill Version(s):

1.15.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
