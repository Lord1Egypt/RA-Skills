## Description: <br>
Remote-control zellij sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jivvei](https://clawhub.ai/user/Jivvei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage interactive Zellij terminal sessions, target panes, send keystrokes, capture pane output, wait for text, and clean up detached sessions while working with command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over local Zellij terminal sessions. <br>
Mitigation: Install it only when that control is intended, use a dedicated data directory, monitor active sessions, and clean up detached sessions after use. <br>
Risk: Pane output may expose sensitive terminal content to the controlling agent. <br>
Mitigation: Avoid targeting panes that display secrets, credentials, or sensitive project output. <br>
Risk: Examples include running no-confirm coding-agent commands in detached sessions. <br>
Mitigation: Allow --yolo or --full-auto style runs only when explicitly requested in a disposable or tightly scoped workspace. <br>


## Reference(s): <br>
- [Zellij documentation](https://zellij.dev) <br>
- [ClawHub skill page](https://clawhub.ai/Jivvei/zellij) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces terminal-control instructions for Zellij sessions and helper script usage; does not itself execute commands unless the host agent follows the guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
