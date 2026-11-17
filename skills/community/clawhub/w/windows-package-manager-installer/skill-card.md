## Description:

Guides agents through Windows software and package-manager installation flows using winget or Chocolatey, including environment checks, package-manager setup, Chocolatey Tsinghua mirror configuration, and verification steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkqiank](https://clawhub.ai/user/darkqiank)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and IT operators use this skill when they want an agent to choose between winget and Chocolatey, provide Windows package-manager setup commands, or produce package-manager-based installation steps for Windows software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PowerShell may install package managers or software and can require administrator rights.

Mitigation: Review every generated command before running it, confirm it matches the installation goal, and run elevated commands only when administrator access is expected.

Risk: Chocolatey setup may install Chocolatey and change Chocolatey package sources to the Tsinghua mirror.

Mitigation: Confirm that Chocolatey installation and the Tsinghua mirror configuration are acceptable for the target environment before executing those steps.

## Reference(s):

- [Package Manager Selection Notes](references/package-selection.md)
- [ClawHub skill page](https://clawhub.ai/darkqiank/skills/windows-package-manager-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command blocks and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese success or failure status text]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
