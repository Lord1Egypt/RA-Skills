## Description:

Dispatch coding tasks to tmux sessions via Sandboxer. Use when you need to spawn Claude Code, Gemini, OpenCode, bash, or lazygit sessions in workspace repos, monitor their progress, or send them commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chriopter](https://clawhub.ai/user/chriopter)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Sandboxer to create, monitor, control, and stop local tmux sessions for coding agents and shell tools inside workspace repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad command, tmux-session, and workspace file-write authority on the host.

Mitigation: Use it only on a dedicated isolated machine where every local process is trusted, preferably under an unprivileged service account.

Risk: Unauthenticated local control can allow unintended workspace changes or commits if exposed beyond trusted local use.

Mitigation: Add authentication, per-workspace authorization, repository allowlists, audit logs, and review before auto-commit or file writes.

Risk: Shared hosts or machines with unrelated sensitive data increase the impact of terminal capture and file access.

Mitigation: Do not deploy it on shared hosts or machines containing sensitive unrelated data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chriopter/skills/sandboxer-tmux)
- [Publisher profile](https://clawhub.ai/user/chriopter)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to issue localhost API calls that create, control, inspect, and terminate tmux-backed sessions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
