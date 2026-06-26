## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor and control existing tmux sessions for interactive terminal applications, including sending input, checking prompts, navigating panes, and reading session output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad read and write control over persistent tmux sessions, including terminal output that may contain sensitive information. <br>
Mitigation: Install only when this control is intended, target known sessions and panes, and avoid panes that may expose secrets. <br>
Risk: Sending keystrokes, Enter, control keys, approvals, kill-session, or other terminal actions can change files or running processes. <br>
Mitigation: Require explicit confirmation before approvals, Enter on prompts, control keys, kill-session, or commands that could alter files or processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utromaya-code/tmux-session-control) <br>
- [Publisher profile](https://clawhub.ai/user/utromaya-code) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [find-sessions.sh](artifact/scripts/find-sessions.sh) <br>
- [wait-for-text.sh](artifact/scripts/wait-for-text.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux and targets existing tmux sessions or panes on Darwin or Linux.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
