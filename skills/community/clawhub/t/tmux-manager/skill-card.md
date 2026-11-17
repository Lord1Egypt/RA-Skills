## Description:

Manage tmux sessions using the tmux-manager.py script to create, kill, restart, list, inspect, send commands to, tail, and validate configured tmux sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rdeangel](https://clawhub.ai/user/rdeangel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define local development environments in YAML and manage tmux sessions, windows, panes, hooks, commands, and inspection workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start, stop, and restart tmux sessions and run commands from YAML configuration.

Mitigation: Review any tmux-sessions.yaml before use, and run --validate, --dry-run, or --list before creating, killing, or restarting sessions.

Risk: Example commands include agent launches that skip approvals.

Mitigation: Remove or replace approval-bypass flags in copied examples unless that behavior is explicitly intended.

Risk: Tailing untrusted or oddly named tmux targets is called out in security guidance.

Mitigation: Avoid --tail on untrusted targets until the temp-file and pipe-pane handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rdeangel/skills/tmux-manager)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local tmux and uv binaries; actions may affect local terminal sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
