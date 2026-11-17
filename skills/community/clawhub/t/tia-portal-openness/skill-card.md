## Description:

Automate TIA Portal via Openness API for PLC project engineering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and controls engineers use this skill to automate Siemens TIA Portal V21 project workflows through PowerShell and the Openness API, including project setup, block export/import, and compile checks for PLC engineering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run PowerShell with elevated privileges.

Mitigation: Review the skill before installing it on an engineering workstation and avoid administrator PowerShell unless Siemens specifically requires it.

Risk: The skill loads the Siemens Openness DLL from a path stored in editable configuration.

Mitigation: Verify references/env.json points to the real local Siemens API directory before running any automation.

Risk: Imported or compiled SCL can change PLC project artifacts.

Mitigation: Run the workflow only against trusted project copies and review generated or modified SCL before import and compile steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/tia-portal-openness)
- [env.json](references/env.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline PowerShell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to guide local TIA Portal automation and SCL project workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
