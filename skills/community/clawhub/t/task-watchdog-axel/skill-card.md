## Description:

Task Watchdog helps agents track task locks, heartbeat freshness, progress timestamps, completion, abandoned sessions, and archive cleanup using external lock files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep task state outside the agent context, update heartbeats and progress at key checkpoints, detect stalled or dead sessions, and archive completed or abandoned tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task records can be taken over, completed, moved, archived, or deleted without reliable ownership checks.

Mitigation: Limit use to a controlled single-user or trusted-agent environment until task and agent IDs are validated and explicit authorization is added for completion, takeover, archive, and cleanup operations.

Risk: Missing identities, failed session-list checks, or fragile parsing can lead to unsafe task ownership decisions.

Mitigation: Require agent and session identity, fail closed when session lookup is unavailable, and use structured JSON parsing before automated or multi-agent deployment.

## Reference(s):

- [Task Watchdog detailed specification](references/spec.md)
- [ClawHub release page](https://clawhub.ai/axelhu/skills/task-watchdog-axel)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; scripts emit terminal text and optional JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts maintain lock files under ~/.openclaw/agents/{agent_id}/locks/ when executed.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
