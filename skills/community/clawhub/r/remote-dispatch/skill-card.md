## Description: <br>
Remote Dispatch turns QQBot remote messages into desktop actions such as screenshots, browser search, clipboard operations, window actions, and file or app opening through a computer-use execution layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxr-666](https://clawhub.ai/user/lxr-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route trusted mobile QQBot messages into desktop-control actions for multi-device workflows, including screenshots, search, clipboard access, window management, and opening files, apps, or URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote-control commands can expose screenshots, clipboard contents, window actions, and file or app opening through broad message triggers. <br>
Mitigation: Install only for a trusted QQBot workflow, enforce sender authentication, require a strict command prefix and the [远程] marker, and confirm sensitive actions before execution. <br>
Risk: Screenshots and clipboard reads may reveal passwords, tokens, private messages, or business data. <br>
Mitigation: Avoid use on systems that may display sensitive information, limit screenshot scope when possible, and review clipboard or screen content before returning it. <br>
Risk: Window closing and file actions can disrupt the desktop session or affect unintended files. <br>
Mitigation: Require explicit confirmation for window closing, clipboard writes, and file actions, and reject ambiguous or destructive requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxr-666/remote-dispatch) <br>
- [Publisher profile](https://clawhub.ai/user/lxr-666) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON action descriptors with human-readable status or confirmation messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe screenshot, browser search, clipboard, window, and open-file/app/URL actions for an agent to execute.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
