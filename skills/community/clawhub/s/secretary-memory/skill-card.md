## Description:

Secretary Memory helps OpenClaw agents operate a partitioned local memory system for session summaries, user preferences, project notes, full-text search, conflict detection, archival, restore, and generated skill suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgj24](https://clawhub.ai/user/wgj24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, search, summarize, archive, and recall local assistant memory across sessions. It is intended for workflows that need persistent project context, user preference tracking, and memory maintenance commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses private conversation data in a persistent local memory system.

Mitigation: Use an isolated non-root memory directory, review recalled context before injecting it into prompts, and periodically inspect or delete stored profile, graph, index, and summary files.

Risk: Automation paths include remote LLM summarization, daemon or watch modes, restore operations, and generated skills.

Mitigation: Disable or avoid those paths unless the configuration and memory directory contents have been reviewed and trusted.

Risk: Stored memories or generated skills can carry prompt-injection or stale-context risk into later sessions.

Mitigation: Review and scan memory content and generated skill files before deployment or reuse.

## Reference(s):

- [Secretary Memory specification](references/SPEC.md)
- [ClawHub skill page](https://clawhub.ai/wgj24/skills/secretary-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local memory artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local profile, graph, index, summary, archive, restore-log, and generated-skill files.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
