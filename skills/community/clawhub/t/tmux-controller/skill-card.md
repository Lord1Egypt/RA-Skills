## Description:

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate interactive terminal sessions through tmux, including launching, sending input to, and capturing output from pane-based CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes examples that run coding agents with approval or permission safeguards disabled.

Mitigation: Use unattended or full-auto agent modes only in an isolated worktree or sandbox when that level of authority is intentional.

Risk: The bundled tmux polling helper is identified by the security evidence as needing hardening for untrusted or generated arguments.

Mitigation: Review and harden script argument handling before using the helper with untrusted inputs.

Risk: tmux pane control can send commands into long-lived interactive sessions.

Mitigation: Inspect the target session and command text before sending input, and prefer literal sends for user-provided command strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brennerspear/skills/tmux-controller)
- [Publisher profile](https://clawhub.ai/user/brennerspear)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on darwin or linux.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
