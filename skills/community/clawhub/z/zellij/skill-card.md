## Description:

Remote-control zellij sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jivvei](https://clawhub.ai/user/jivvei)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when an agent needs an interactive terminal workspace for Zellij sessions, including launching panes, sending keystrokes, reading pane output, polling for prompts, and cleaning up sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can control Zellij sessions and send keystrokes into interactive terminal panes.

Mitigation: Install only when agent control of Zellij sessions is intended, and run it in a workspace with appropriate command approvals and restricted credentials.

Risk: The skill documents unattended agent patterns using approval bypass flags and helper scripts may expose full pane output.

Mitigation: Avoid approval bypass modes except in disposable isolated workspaces, review resulting changes, and treat captured pane output as sensitive.

## Reference(s):

- [Zellij documentation](https://zellij.dev)
- [ClawHub skill page](https://clawhub.ai/jivvei/skills/zellij)
- [Publisher profile](https://clawhub.ai/user/jivvei)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and helper script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires zellij and jq on PATH; intended for macOS and Linux environments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
