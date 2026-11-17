## Description:

Session Continuity helps an OpenClaw agent save named checkpoints for unfinished work and resume from task-level state after session end, context loss, compaction, or crashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preserve multi-step task state before a session ends and to resume work from a structured checkpoint instead of reconstructing prior context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local checkpoint files may retain sensitive project context across sessions.

Mitigation: Review checkpoint contents before use, avoid saving secrets or personal data, and purge stale autosave or named checkpoint files when they are no longer needed.

Risk: Unvalidated checkpoint names may allow read, overwrite, or delete operations outside the intended checkpoint folder.

Mitigation: Restrict checkpoint names to safe kebab-case identifiers and fix path validation before enabling resume or delete commands in sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/session-continuity)
- [Checkpoint Format](references/checkpoint-format.md)
- [Resume Flow](references/resume-flow.md)
- [Auto-Checkpoint Signals](references/auto-checkpoint-signals.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [proactive-agent WAL Protocol inspiration](https://github.com/hal-lobster/proactive-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checkpoint briefings, checkpoint files, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checkpoint content is persisted as local Markdown files under the workspace memory/checkpoints directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
