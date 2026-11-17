## Description:

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyaya100](https://clawhub.ai/user/zhouyaya100)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to control interactive tmux-backed CLI sessions, monitor pane output, find sessions, and wait for expected terminal text during agent or REPL workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to run unattended coding commands with broad authority.

Mitigation: Avoid `--yolo` or `--full-auto` unless the agent is isolated in a disposable worktree or container with no personal credentials.

Risk: Timeout diagnostics may print captured terminal contents.

Mitigation: Use the helpers only on tmux sessions intended for agent control, and avoid capturing panes that may contain secrets or sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouyaya100/skills/tmux-temp)
- [Publisher profile](https://clawhub.ai/user/zhouyaya100)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on PATH; supports macOS and Linux, with Windows use through WSL.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
