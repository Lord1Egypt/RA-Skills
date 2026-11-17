## Description:

多端协同/Dispatch 远程桌面操控。受 Claude Dispatch 功能启发——手机发指令，电脑执行。将 QQBot 收到的远程指令转化为 desktop actions：截图回传、打开浏览器搜索、操作桌面应用、文件操作。需要 computer-use skill 配合使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxr-666](https://clawhub.ai/user/lxr-666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route authorized QQBot remote commands into desktop actions such as screenshots, browser search, clipboard access, window management, and file or app opening through a downstream computer-use executor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote desktop actions may be triggered from broad chat phrases without enforcing the documented [远程] marker.

Mitigation: Require strict sender authentication, require the [远程] prefix, and use an explicit command grammar before passing actions to the desktop executor.

Risk: Screen, clipboard, and window actions can expose private information or affect active desktop work.

Mitigation: Confirm screenshot, clipboard, and window-close actions before execution and restrict use to a QQBot channel and computer-use executor controlled by the installer.

Risk: Open-target actions can launch URLs, applications, or files selected through chat input.

Mitigation: Restrict allowed URLs, apps, and file paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxr-666/skills/remote-dispatch)
- [Publisher profile](https://clawhub.ai/user/lxr-666)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON action payloads with human-facing status or confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit screenshot, search, clipboard, window, open-target, and confirmation actions for downstream desktop execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
