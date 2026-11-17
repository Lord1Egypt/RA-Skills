## Description:

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage tmux sessions for interactive terminal workflows, including launching, monitoring, sending input to, and cleaning up remote-control CLI sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents running autonomous coding agents with approval safeguards disabled.

Mitigation: Use bypass or full-auto flags only in a tightly scoped sandbox or throwaway worktree, and review resulting changes before merging or deployment.

Risk: The bundled wait helper needs numeric input validation before use with untrusted automation inputs.

Mitigation: Validate timeout, interval, stale, and line-count arguments as numeric values before passing them to the helper in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brennerspear/skills/tmux-remote-control)
- [Publisher profile](https://clawhub.ai/user/brennerspear)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on macOS or Linux.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
