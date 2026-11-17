## Description:

Operates XCP-ng fleets through Xen Orchestra for health checks, root-cause analysis, and governed VM, storage, and snapshot actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and virtualization operators use this skill to inspect XCP-ng health, diagnose VM, storage, backup, and pool issues, and perform governed operations through Xen Orchestra.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP write calls may not prompt for user confirmation, and snapshot deletion or reversion cannot be undone.

Mitigation: Use a dedicated read-only Xen Orchestra account until writes are needed; require client-side approval for the exact operation and target before enabling MCP writes, and review dry-run previews before destructive CLI actions.

Risk: Stopping the VM that hosts Xen Orchestra can interrupt management access when that VM is not declared to the skill.

Mitigation: Configure xo_self_vm_uuid for the target and test operations outside production first.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zw008/skills/xcpng-aiops)
- [Project homepage](https://github.com/AIops-tools/XCPng-AIops)
- [Capabilities reference](artifact/references/capabilities.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [CLI reference](artifact/references/cli-reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Shell commands]

**Output Format:** [Concise operational summaries and guidance with structured JSON tool results and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results reflect the configured Xen Orchestra environment; findings depend on the data returned by Xen Orchestra.]

## Skill Version(s):

0.11.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
