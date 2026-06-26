## Description: <br>
Production-grade memory persistence and lifecycle management for VM-hosted OpenClaw agents using a local 4-layer memory architecture with activation decay, nightly consolidation, health monitoring, and self-healing maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharoonsharif](https://clawhub.ai/user/sharoonsharif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to maintain persistent local memory for OpenClaw agents on Linux VMs, including fact ingestion, daily summaries, recall, consolidation, pruning, cron-based maintenance, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags persistent VM-level cron jobs as requiring review. <br>
Mitigation: Review or disable the cron setup before deployment and confirm the installed schedule matches operational expectations. <br>
Risk: The security review notes weak scoping for sensitive memory storage. <br>
Mitigation: Restrict permissions on /data/memory before storing session history and avoid writing secrets or credentials into memory files. <br>
Risk: Automated consolidation can prune or clean retained memory data. <br>
Mitigation: Confirm retention deletion is acceptable and keep backups or disk snapshots before enabling automated consolidation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sharoonsharif/vm-memory-oracle) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Basic Usage Guide](examples/basic-usage.md) <br>
- [Azure Fleet Deployment Guide](examples/azure-fleet-deployment.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell, JSON, YAML, and configuration examples for local memory files and VM maintenance tasks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local filesystem memory artifacts such as JSONL fact stores, Markdown summaries, health JSON, cron configuration, and rebuildable embedding indexes.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
