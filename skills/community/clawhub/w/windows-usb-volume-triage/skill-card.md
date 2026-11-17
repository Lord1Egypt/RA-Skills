## Description:

Diagnose missing Windows USB volumes or mount paths safely with read-only disk, partition, volume, and PnP correlation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators, support engineers, and Windows storage operators use this skill to diagnose USB disks or enclosures where Windows detects hardware but an expected drive letter or directory mount is missing. It guides read-only correlation across disks, partitions, volumes, and PnP device evidence before any repair decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic output may include hardware identifiers such as serial numbers and device paths.

Mitigation: Treat collected identifiers as operationally sensitive and share them only with trusted administrators or support channels.

Risk: Using the workflow outside read-only triage could lead to destructive storage actions.

Mitigation: Keep the no-initialize and no-format guidance intact, and require explicit user approval before any repair or write action.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic workflow; may include selected Windows disk, partition, volume, and PnP fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
