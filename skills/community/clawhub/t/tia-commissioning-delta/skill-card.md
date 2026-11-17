## Description:

Use TIA Openness to compare latest site backup against yesterday's baseline with focus on process control logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjmore66](https://clawhub.ai/user/cjmore66)

### License/Terms of Use:

MIT-0

## Use Case:

Field engineers and commissioning teams use this skill to compare Siemens TIA Portal backup archives and summarize significant control-logic changes across safety blocks, PID controllers, sequences, and alarms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may invoke an external PowerShell or TIA Openness diff script that is not shipped or validated with the release.

Mitigation: Confirm the external script comes from a trusted source and run it only against intended backup archives.

Risk: Diff output may identify safety, interlock, PID, sequence, or alarm changes that could affect commissioning decisions.

Mitigation: Have a qualified field engineer review the reported changes against the original TIA Portal backups before acting on them.

## Reference(s):

- [TIA Commissioning Delta Scripts](Scripts/README.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Analysis, Guidance]

**Output Format:** [Compact JSON summary with supporting Markdown or shell command guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on changed PIDs, bypassed interlocks, changed sequences, alarms, summary counts, risk levels, block names, and descriptions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
