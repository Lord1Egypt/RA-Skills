## Description:

Monitor host system health (Disk, RAM, CPU). Returns structured JSON status for predictive maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[numbpill3d](https://clawhub.ai/user/numbpill3d)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run a local host health check and receive structured status about disk, memory, and load conditions before resource exhaustion causes failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads basic local host resource information.

Mitigation: Install and run it only in environments where reading disk, memory, and load metrics is acceptable.

Risk: The CPU metric is load average rather than CPU percentage.

Mitigation: Interpret the reported CPU value as 15-minute load average and avoid comparing it directly to percentage thresholds.

Risk: The documented example output does not exactly match the script's actual JSON shape.

Mitigation: Integrations should parse the script's actual top-level status, metrics, and warnings fields.

## Reference(s):

- [System Vigil on ClawHub](https://clawhub.ai/numbpill3d/skills/system-vigil)
- [Publisher profile: numbpill3d](https://clawhub.ai/user/numbpill3d)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON report printed by a Python script, with Markdown usage guidance for the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local access to standard Linux utilities: df, free, and uptime.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
