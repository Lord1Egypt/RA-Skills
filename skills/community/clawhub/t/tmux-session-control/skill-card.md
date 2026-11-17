## Description:

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and control existing tmux sessions for interactive terminal workflows, including monitoring agent sessions, sending input, and capturing pane output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sending keys, approving prompts, interrupting jobs, or killing sessions can affect active work if the wrong tmux target is selected.

Mitigation: Verify the target session, window, and pane before performing control actions.

Risk: Captured pane output may contain sensitive terminal content.

Mitigation: Capture only the needed pane history and review terminal output before sharing or storing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/tmux-session-control)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on macOS or Linux.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
