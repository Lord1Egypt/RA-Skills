## Description:

A clean, reliable system resource monitor for CPU load, RAM, Swap, and Disk usage, optimized for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[passersss](https://clawhub.ai/user/passersss)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to answer system health questions by running a local, read-only resource report for CPU load, memory, swap, disk usage, and uptime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad requests such as system status or server health could invoke local metric collection unintentionally.

Mitigation: Use the skill only when local system health reporting is expected, and review agent routing for broad system-status phrases.

Risk: The skill exposes basic local machine resource status to the requesting agent session.

Mitigation: Deploy only where sharing CPU, memory, swap, disk, and uptime information with the agent is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/passersss/skills/system-resource-monitor)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or terminal-style text summarizing local system resource metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local uptime, CPU load averages, RAM usage, swap usage, and root disk usage.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
