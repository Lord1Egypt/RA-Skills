## Description:

Windows 桌面控制工具 (仅Windows) - 截屏、窗口管理、鼠标键盘控制、进程管理、系统信息。当用户要求截屏、查看进程、关闭程序、桌面控制时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tr0812](https://clawhub.ai/user/tr0812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this Windows-only skill to let an agent inspect and control a local desktop through screenshots, process listing, mouse and keyboard actions, clipboard access, and system information commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue desktop actions such as clipboard, keyboard, mouse, screenshot, and process-kill operations with broad local authority.

Mitigation: Use only in a trusted local Windows environment, avoid administrator privileges, and require human approval before high-impact desktop or process actions.

Risk: Security evidence identifies clipboard command injection risk through PowerShell clipboard input.

Mitigation: Do not allow untrusted prompts or content to invoke clipboard writes; publisher should fix command construction before broad use.

Risk: Security evidence states process-kill behavior may terminate unintended processes.

Mitigation: Enforce the process allowlist for all process identifiers and review requested process termination before execution.

Risk: Dependencies are not pinned in the artifact documentation.

Mitigation: Pin and review Python dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tr0812/skills/windows-desktop-control)
- [Publisher profile](https://clawhub.ai/user/tr0812)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON command results and generated screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are saved under ~/Pictures/OpenClaw/ and command results are printed as JSON.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
