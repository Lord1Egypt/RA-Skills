## Description:

Develop, run, and troubleshoot Python programs for the UNIHIKER M10 from Windows or macOS with the unihiker and PinPong APIs, including display, sensor, GPIO, audio, SSH deployment, environment selection, and offline dependency workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick-ccq](https://clawhub.ai/user/nick-ccq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and hardware builders use this skill to generate, deploy, and troubleshoot Python programs for UNIHIKER M10 devices from Windows or macOS. It helps select a board Python environment, use M10 display and hardware APIs, deploy over SSH/SCP, and install missing dependencies when the board lacks Internet access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses SSH/SCP deployment and package installation paths that can make root-level changes on an M10 device.

Mitigation: Confirm the target board connection and intended action before device-changing operations, change factory-default credentials, and grant SSH/SCP access only to agents and users trusted to modify the device.

Risk: The security evidence reports a confirmed PowerShell package-install injection risk in the -PipInstall path.

Mitigation: Review every package name before installation, prefer pinned versions from trusted sources, and avoid the PowerShell -PipInstall path until package values are quoted or strictly validated.

Risk: Generated or example programs may record audio or terminate running processes.

Mitigation: Confirm recording and process-termination intent with the device owner and use narrow process targets rather than broad commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nick-ccq/skills/unihiker-m10-python)
- [Project homepage](https://github.com/Nick-ccq/unihiker-m10-python)
- [Connection guide](references/connection-guide.md)
- [Python environments](references/m10-python-env.md)
- [Hardware reference](references/m10-hardware.md)
- [UNIHIKER and PinPong API](references/unihiker-pinpong-api.md)
- [Code templates](references/code-templates.md)
- [Offline dependencies](references/offline-dependencies.md)
- [macOS workflow](references/macos-workflow.md)
- [UNIHIKER M10 documentation](https://www.unihiker.com.cn/wiki/m10/)
- [M10 image documentation](https://www.unihiker.com.cn/wiki/m10/burner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Python programs, .m10-env.json configuration, troubleshooting steps, and SSH/SCP deployment commands for the selected M10 environment.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
