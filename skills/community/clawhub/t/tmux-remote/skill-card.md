## Description:

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[164149043](https://clawhub.ai/user/164149043)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage interactive command-line workflows inside tmux, including listing sessions, attaching to panes, sending commands, capturing pane output, and waiting for expected text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate live tmux panes, including sending input and killing panes.

Mitigation: Use dedicated session names and verify the target session, window, and pane before sending keys or killing panes.

Risk: Captured pane output can include secrets, credentials, or private terminal history.

Mitigation: Avoid capturing sensitive panes and review pane output before sharing or storing it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell script helpers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on Linux or macOS; helper scripts can list sessions and poll pane output for matching text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
