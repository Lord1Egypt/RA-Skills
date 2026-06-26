## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[securecloudprojo](https://clawhub.ai/user/securecloudprojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when an interactive TTY is needed for tmux-backed CLI sessions, including sending keystrokes, watching pane output, and managing multiple agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to launch other coding agents in unattended modes. <br>
Mitigation: Use isolated git worktrees, avoid unattended subagents unless explicitly intended, and inspect diffs before keeping changes. <br>
Risk: Capturing tmux panes can expose terminal history that may contain sensitive text. <br>
Mitigation: Avoid capturing panes that may contain secrets and kill tmux sessions or sockets when finished. <br>
Risk: Interactive tmux automation can keep commands running after the initiating task appears complete. <br>
Mitigation: Monitor sessions with tmux attach or capture-pane commands and clean up sessions with kill-session or kill-server. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/securecloudprojo/tmux-steipete) <br>
- [Publisher profile](https://clawhub.ai/user/securecloudprojo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on PATH and is gated to macOS and Linux.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
