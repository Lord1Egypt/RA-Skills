## Description:

开箱即用的Windows桌面GUI自动化集成技能，整合原生UI自动化、鼠标控制、截图识别、AI视觉分析，一站式解决Windows桌面自动化需求。支持打开应用、点击、输入、截图、OCR识别、流程自动化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiatian5](https://clawhub.ai/user/xiatian5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, and operations users use this skill to plan Windows desktop automation workflows for launching applications, locating controls, clicking, typing, capturing screenshots, OCR, and AI-assisted visual analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad desktop control can perform unintended clicking or typing in active Windows sessions.

Mitigation: Use a dedicated, least-privileged Windows session and require confirmation before actions that click, type, or operate applications.

Risk: Screenshots, OCR output, AI visual analysis, and logs may expose sensitive on-screen information.

Mitigation: Close sensitive windows before use and treat captured images, OCR text, AI analysis, and logs as sensitive data.

Risk: The skill depends on multiple automation skills that affect desktop control behavior.

Mitigation: Pin and verify dependent automation skills where possible before installing or running workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiatian5/skills/windows-gui-automation-cn)
- [windows-ui-automation](https://clawhub.ai/skills/windows-ui-automation)
- [win-mouse-native](https://clawhub.ai/skills/win-mouse-native)
- [midscene-computer-automation](https://clawhub.ai/skills/midscene-computer-automation)
- [windows-rpa](https://clawhub.ai/skills/windows-rpa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline PowerShell examples and workflow templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for coordinating dependent Windows automation skills; no standalone executable artifact is provided.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
