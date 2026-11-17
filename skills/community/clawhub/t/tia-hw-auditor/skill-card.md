## Description:

Use TIA Openness to compare hardware and I/O configuration between field and master backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjmore66](https://clawhub.ai/user/cjmore66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Siemens TIA Portal hardware and I/O differences between field and master backups. It helps identify device additions or removals, address shifts, firmware changes, and module changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access engineering network shares and backup files.

Mitigation: Use explicitly configured NAS and vault paths and grant read-only access to required backup files.

Risk: The skill can run an external TIA Openness audit script.

Mitigation: Use a trusted, version-pinned audit script and review it before installation or execution.

Risk: Heartbeat-triggered runs may execute audits automatically.

Mitigation: Require clear approval or monitoring for heartbeat-triggered runs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Analysis, Configuration instructions]

**Output Format:** [Markdown guidance with PowerShell commands, CSV output, and JSON summary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hardware-diff.csv for detailed changes and summary.json for agent consumption.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
