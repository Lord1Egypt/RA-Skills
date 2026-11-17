## Description:

Provides governed TrueNAS SCALE storage operations, including health checks, diagnostics, pool and dataset inspection, snapshot management, disk health, alerts, services, and replication status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT

## Use Case:

TrueNAS SCALE administrators use the skill to inspect appliance health and storage state, investigate pool or alert issues, and carry out supported maintenance actions through an agent or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snapshot deletion through MCP is irreversible; audit records and risk labels do not prevent deletion, and dependent clones may also be affected.

Mitigation: Start with an appliance account that cannot write. Before granting write access, require explicit approval for each destructive MCP action and confirm the exact snapshot and its dependencies.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zw008/skills/truenas-aiops)
- [Project homepage](https://github.com/AIops-tools/TrueNAS-AIops)
- [Capabilities](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup and security guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Text, Shell commands, Configuration instructions]

**Output Format:** [Structured results and concise operational guidance, with CLI commands when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include explicit null fields and truncation indicators.]

## Skill Version(s):

0.14.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
