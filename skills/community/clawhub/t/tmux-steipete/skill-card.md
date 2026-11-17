## Description:

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[securecloudprojo](https://clawhub.ai/user/securecloudprojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs an interactive TTY to control tmux sessions, send input, monitor pane output, and coordinate interactive CLI work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended coding-agent runs with reduced approval safeguards can make unreviewed changes.

Mitigation: Use isolated worktrees or disposable environments, avoid reduced-safeguard examples unless necessary, and review all changes afterward.

Risk: Cleanup commands can terminate active tmux jobs.

Mitigation: Verify the target socket and session before cleanup, and avoid broad kill commands when unrelated sessions may be active.

Risk: Capturing tmux pane output can expose sensitive terminal content.

Mitigation: Limit capture history to what is needed and avoid running the skill in panes that display secrets or private data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/securecloudprojo/skills/tmux-steipete)
- [Publisher profile](https://clawhub.ai/user/securecloudprojo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and helper script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on PATH and is gated for macOS and Linux environments.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
