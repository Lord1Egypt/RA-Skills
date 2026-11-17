## Description:

Manage background coding agents in tmux sessions. Spawn Claude Code or other agents, check progress, get results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuba6112](https://clawhub.ai/user/cuba6112)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to start, monitor, inspect, and manage coding agents running in persistent tmux sessions for background implementation, refactoring, research, documentation, and test-writing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can start coding agents with unattended high-impact control over the workspace.

Mitigation: Use disposable or tightly scoped workspaces, prefer interactive modes unless unattended edits are intentional, and review agent changes before relying on them.

Risk: Shell input handling may be unsafe when session names, agent names, or task text come from untrusted sources.

Mitigation: Avoid untrusted task text and use only trusted session and agent identifiers when spawning sessions.

Risk: Cloud agent variants may send prompts, code, and task context to external providers.

Mitigation: Avoid sending sensitive data to cloud agents unless provider use is approved; choose local Ollama variants when local execution is required.

Risk: Persistent tmux sessions can continue running after the user leaves the workflow.

Mitigation: Check active sessions and kill tmux sessions when work is finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuba6112/skills/tmux-agents)
- [Skill homepage](https://clawdhub.com/skills/tmux-agents)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux; local agent variants require Ollama setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
