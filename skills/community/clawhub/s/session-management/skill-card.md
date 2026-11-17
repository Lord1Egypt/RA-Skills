## Description:

Structured session lifecycle for Claude Code - start, checkpoint, end, and daily heartbeat commands that maintain project state across conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to start sessions with prior project context, checkpoint progress, close sessions with durable notes, and run daily heartbeat checks for stale state, blockers, deadlines, and memory updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session state, session logs, and approved memory entries can preserve project details that may be sensitive if committed or shared.

Mitigation: Install only where durable session notes are acceptable, and review content written to state/, sessions/, and approved MEMORY.md entries before committing or sharing the repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/session-management)
- [Session Management README](README.md)
- [Session Management Skill Definition](SKILL.md)
- [Agent Workspace canonical home](https://github.com/conorbronsdon/agent-workspace)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and project-state file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces briefings, checkpoints, session summaries, state-file updates, and memory proposals as user-invoked session lifecycle output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
