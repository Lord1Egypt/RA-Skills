## Description: <br>
Tmux会话工具免费版 helps personal developers manage a single tmux session by locating panes, reading recent pane output, sending commands, and dumping buffers for debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and control a tmux pane in a personal development environment, especially when interacting with a code assistant running inside tmux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read terminal pane contents and type into panes, which may expose sensitive output or run unintended commands if the wrong target is selected. <br>
Mitigation: Confirm the exact tmux session, window, and pane before reading or sending input, and avoid panes that show credentials, customer data, private prompts, or production shells unless that access is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tmux-session-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with tmux command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed, running tmux session; the free edition focuses on one session at a time.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
