## Description:

Kannaka Memory helps agents operate a persistent HRM memory system for storing, recalling, forgetting, consolidating, snapshotting, restoring, and synchronizing memories across a NATS-backed swarm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage durable Kannaka memories, perform recall and consolidation, coordinate swarm memory behavior, recover from snapshots, and configure LLM-backed ask/chat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory and restore operations can change or replace persisted agent memory.

Mitigation: Require explicit approval for forget, prune, dream, restore, and similar state-changing actions, and prefer dry-run or backup flows before applying changes.

Risk: Swarm, NATS, and remote restore workflows can contact peers or remote endpoints.

Mitigation: Limit NATS brokers and restore URLs to systems you control, and review network targets before starting long-lived services.

Risk: LLM provider configuration may involve API keys or other credentials.

Mitigation: Prefer environment variables or a secret manager for API keys instead of storing credentials in local configuration.

Risk: Update and orchestration guidance can lead to unpinned installs or additional tools.

Mitigation: Review install commands and pin trusted package versions before allowing global installs or delegated orchestration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/skill-kannaka-memory)
- [Publisher profile](https://clawhub.ai/user/nickflach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide durable memory, networked swarm, snapshot, restore, and LLM provider configuration actions.]

## Skill Version(s):

2.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
