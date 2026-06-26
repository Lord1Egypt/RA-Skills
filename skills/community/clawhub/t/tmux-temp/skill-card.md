## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouyaya100](https://clawhub.ai/user/zhouyaya100) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to work with interactive terminal programs through tmux sessions, including starting sessions, sending input, capturing pane output, waiting for text, and cleaning up sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad and persistent control over local tmux sessions. <br>
Mitigation: Use isolated sockets, keep work limited to named directories, monitor detached sessions, and require explicit approval before sending commands. <br>
Risk: Pane capture or automated command entry could expose secrets or affect important running work. <br>
Mitigation: Avoid panes containing secrets, review captured output carefully, and confirm no important work is running before cleanup. <br>
Risk: Non-interactive agent runs with elevated autonomy can execute unintended changes. <br>
Mitigation: Require explicit approval before using autonomous modes such as --yolo or --full-auto. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhouyaya100/tmux-temp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and helper-script usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on PATH and targets macOS or Linux environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
