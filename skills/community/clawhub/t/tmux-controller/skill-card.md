## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when an agent needs to operate an interactive TTY workflow through tmux, including creating sessions, sending input, capturing pane output, and waiting for text patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to control tmux sessions, send shell input, and capture pane output, which can expose or act on sensitive terminal state. <br>
Mitigation: Install only when tmux control is intended, avoid capturing panes with secrets, and run work in isolated worktrees or disposable projects when possible. <br>
Risk: The skill examples normalize unattended coding-agent modes that bypass permission prompts. <br>
Mitigation: Avoid permission-bypassing and full-auto examples unless unattended code and shell changes are explicitly acceptable. <br>
Risk: Bulk cleanup commands can terminate multiple managed tmux sessions. <br>
Mitigation: List `oc-*` sessions before running bulk cleanup and kill only the sessions intended for removal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrennerSpear/tmux-controller) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes tmux session naming, pane targeting, command-sending, output capture, polling, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
