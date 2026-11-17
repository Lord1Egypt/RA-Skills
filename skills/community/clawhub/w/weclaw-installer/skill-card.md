## Description:

Automate installing and configuring the WeClaw WeChat bot environment on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popilopi168](https://clawhub.ai/user/popilopi168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users setting up WeClaw use this skill to install the local macOS environment, configure required dependencies, provide the needed API key, and recover from common macOS Accessibility permission blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup wrapper can load Python code from outside the packaged skill.

Mitigation: Run it only from a trusted checkout after inspecting setup_package.py and the target repository.

Risk: The setup process may handle a WeClaw API key.

Mitigation: Avoid passing real API keys on the command line when possible and provide only the key required for WeClaw setup.

Risk: macOS Accessibility permission grants desktop automation control to the terminal or agent.

Mitigation: Enable the permission only when you are comfortable granting that control for WeClaw setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/popilopi168/skills/weclaw-installer)
- [Publisher profile](https://clawhub.ai/user/popilopi168)
- [WeClaw source repository](https://github.com/Popilopi168/weclaw-package-upload-test)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for a WeClaw API key and macOS Accessibility confirmation before running setup.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
