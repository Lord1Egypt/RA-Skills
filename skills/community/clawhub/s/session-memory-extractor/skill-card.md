## Description:

Scans old OpenClaw session files, uses AI to extract durable decisions, preferences, facts, and tasks into memory/, then cleans up source session files while quarantining failed extractions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmqiang-711](https://clawhub.ai/user/lmqiang-711)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to convert older .jsonl and .trajectory.jsonl session history into persistent memory entries before removing or quarantining the original session files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private session history may be sent to MiniMax and persisted into memory files.

Mitigation: Use only on agents whose old sessions are acceptable for external processing, run preview or dry-run first, and review or skip sessions that may contain secrets or sensitive business content.

Risk: Normal execution can permanently remove raw session history after writing summarized memories.

Mitigation: Keep backups, use dry-run review workflows before normal execution, and confirm that quarantine logs preserve failed extraction cases for audit.

Risk: Feishu notifications can expose extracted summaries to unintended recipients.

Mitigation: Keep Feishu notifications disabled unless the recipient or webhook target is trusted and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lmqiang-711/skills/session-memory-extractor)
- [ClawHub metadata homepage](https://clawhub.ai/hasakyi/session-memory-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown memory entries, console summaries, JSON reports, and optional notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send session content to MiniMax, append extracted memories to memory/YYYY-MM-DD.md, write quarantine audit logs, and delete successfully processed raw session files.]

## Skill Version(s):

1.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
