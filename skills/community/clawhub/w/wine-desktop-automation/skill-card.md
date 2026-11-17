## Description:

Controls desktop applications with mouse and keyboard automation for GUI operations, desktop software control, and UI testing in Ubuntu + Wine environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaodu](https://clawhub.ai/user/xiaodu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate Linux and Wine-hosted Windows GUI workflows, including UI testing, image-based control, window management, and repetitive desktop tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live desktop control can affect active applications or sensitive windows.

Mitigation: Run automation in a dedicated test desktop or VM when possible, and keep sensitive windows closed before execution.

Risk: The skill can launch applications, close or kill windows and processes, and change Wine prefixes.

Mitigation: Review automation scripts before use and require explicit target applications, windows, processes, and prefixes for destructive actions.

Risk: Screenshot and image-recognition workflows may capture sensitive on-screen information.

Mitigation: Limit capture to the required screen region where possible and avoid running the skill while confidential content is visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaodu/skills/wine-desktop-automation)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
