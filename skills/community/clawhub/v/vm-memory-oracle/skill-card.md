## Description:

Production-grade memory persistence and lifecycle management for VM-hosted OpenClaw agents, using a local 4-layer memory architecture with a knowledge graph, semantic index, daily summaries, canonical memory, activation and decay scoring, consolidation, and health monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharoonsharif](https://clawhub.ai/user/sharoonsharif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain persistent local memory for VM-hosted OpenClaw agents, including fact ingestion, recall, scheduled consolidation, pruning, backups, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent memory and raw session logs can retain sensitive user or operational data.

Mitigation: Use a dedicated unprivileged account, restrict /data/memory permissions, avoid storing sensitive raw logs unless users consent, and provide a deletion path.

Risk: Cron setup may affect a shared or production VM outside the declared filesystem scope.

Mitigation: Verify the installed cron file, confirm which user runs each scheduled job, and review the configuration before production installation.

## Reference(s):

- [VM Memory Oracle README](artifact/README.md)
- [Security Policy](artifact/SECURITY.md)
- [Basic Usage Examples](artifact/examples/basic-usage.md)
- [Azure Fleet Deployment Guide](artifact/examples/azure-fleet-deployment.md)
- [Cloud-init VM Template](artifact/examples/vm-cloud-init.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, YAML configuration, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local filesystem and cron lifecycle guidance for OpenClaw agent memory operations.]

## Skill Version(s):

2.0.0 (source: frontmatter, openclaw.plugin.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
