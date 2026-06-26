## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to manage interactive tmux sessions for CLIs, send keystrokes, capture pane output, wait for prompts, and coordinate multiple agent sessions on macOS or Linux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent control tmux sessions and run interactive commands without further prompts. <br>
Mitigation: Use a private tmux socket, approve the task and workspace before unattended runs, avoid --yolo or --full-auto unless explicitly intended, and review diffs before accepting changes. <br>
Risk: Pane capture and wait helpers can expose recent terminal output, including sensitive text visible in tmux panes. <br>
Mitigation: Avoid sensitive panes when capturing output or waiting for text, keep sessions on a private socket, and kill tmux sessions when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/tmux) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on PATH; supports macOS and Linux.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
