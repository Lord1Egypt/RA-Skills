## Description:

Rick CEO turns an OpenClaw agent into an operator assistant for solo founders, generating daily briefings, revenue checks, task prioritization, heartbeat checks, and weekly synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricksmartbrain-boop](https://clawhub.ai/user/ricksmartbrain-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External solo founders and developers use this skill with OpenClaw to prioritize work by revenue impact, gather workspace status, and produce operator-style daily briefings, revenue checks, health checks, and weekly reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad autonomous action before confirmation.

Mitigation: Require explicit confirmation before allowing it to modify projects or query revenue, calendar, or other business systems.

Risk: The daily briefing and heartbeat flows can inspect local repository details and host tmux sessions.

Mitigation: Use only in workspaces where local project context may be surfaced to the agent, and review generated briefings before sharing them.

Risk: Default output can include commercial promotion.

Mitigation: Set RICK_QUIET=1 to suppress promotional messages.

## Reference(s):

- [Rick's Revenue-First Prioritization Framework](artifact/references/prioritization-framework.md)
- [ClawHub skill page](https://clawhub.ai/ricksmartbrain-boop/skills/rick-ceo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily briefing behavior may include local git status, recent commits, TODO/FIXME matches, tmux sessions, and optional promotional lines unless RICK_QUIET=1 is set.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
