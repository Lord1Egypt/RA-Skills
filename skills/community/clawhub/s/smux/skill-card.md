## Description:

Cross-pane messaging for tmux using the `tmux-bridge` command to send messages between panes labeled p1, p2, p3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkuiwu](https://clawhub.ai/user/mkuiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Smux to coordinate work across multiple tmux panes, send tasks or status messages to labeled panes, and route expected replies between collaborating agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-pane reply routing can disclose final results to another pane based on mutable tmux state.

Mitigation: Check `tmux-bridge pending` before replying and use `reply` only for intentional `--expect-reply` requests in trusted panes.

Risk: Session management commands can close an entire tmux session when the wrong session name is supplied.

Mitigation: Confirm session names before using `tmux-bridge kill-session` or `tmux-bridge -k`.

Risk: Auto-label setup appends configuration to `~/.tmux.conf`.

Mitigation: Review generated `auto-label` configuration before appending it and reloading tmux.

## Reference(s):

- [Smux ClawHub skill page](https://clawhub.ai/mkuiwu/skills/smux)
- [mkuiwu ClawHub publisher profile](https://clawhub.ai/user/mkuiwu)
- [tmux-bridge](references/tmux-bridge.md)
- [tmux](references/tmux.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on Darwin or Linux and uses labeled tmux panes for routing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
