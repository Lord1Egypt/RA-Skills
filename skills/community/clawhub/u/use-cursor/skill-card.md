## Description:

Manage Cursor CLI tasks via tmux with security hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucezhu888](https://clawhub.ai/user/brucezhu888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to start, monitor, control, and stop Cursor CLI coding tasks in tmux from OpenClaw workflows, including long-running refactors, reviews, and diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad terminal-control behavior can affect local tmux sessions or expose workspace output when used on sensitive machines.

Mitigation: Install only after review, preferably in a container or disposable development environment, and avoid machines with valuable secrets or unrelated tmux work.

Risk: Normal operation can run Cursor through tmux with access to the working environment.

Mitigation: Prefer isolated mode for sensitive projects and review task strings before sending them to a running session.

Risk: Installer guidance may involve remote shell scripts.

Mitigation: Independently verify installer commands before execution instead of following curl-to-bash guidance directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucezhu888/skills/use-cursor)
- [ClawHub publisher profile](https://clawhub.ai/user/brucezhu888)
- [OpenClaw skills homepage](https://github.com/openclaw/skills)
- [Cursor official docs](https://cursor.com/docs)
- [Cursor CLI GitHub](https://github.com/getcursor/cursor)
- [tmux usage guide](https://github.com/tmux/tmux/wiki)
- [OpenClaw ACP docs](https://docs.openclaw.ai/cli/acp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON-like tool results and plain text status or output captured from tmux]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session identifiers, task status, tmux output, and diagnostic results.]

## Skill Version(s):

1.0.11 (source: ClawHub release evidence; artifact files report 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
