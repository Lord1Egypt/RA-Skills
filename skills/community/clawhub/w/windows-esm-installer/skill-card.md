## Description:

Helps Windows users diagnose and repair OpenClaw/Skill installation issues by fixing local path URLs, configuring npm registry settings, checking dependencies, and generating install scripts and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to troubleshoot Windows-specific OpenClaw/Skill installation failures, including ESM path errors, npm download issues, and missing local dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change npm registry configuration to npmmirror.com.

Mitigation: Run diagnostic mode first, confirm the registry change is acceptable, and restore the registry after use if the environment requires another source.

Risk: The skill can overwrite install.bat, install.ps1, or INSTALL_REPORT.md in the current working directory.

Mitigation: Run it only in the intended project directory and check for existing files before repair.

Risk: Generated install scripts run npm install and may be suggested for elevated execution.

Mitigation: Review generated scripts before running them and avoid Administrator execution unless the user explicitly accepts that need.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/windows-esm-installer)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated Windows batch and PowerShell scripts plus shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write install.bat, install.ps1, and INSTALL_REPORT.md in the working directory and may set npm registry configuration to npmmirror.com during repair.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
