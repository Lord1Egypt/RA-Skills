## Description:

A clean, reliable system resource monitor for CPU load, RAM, Swap, and Disk usage, optimized for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nguyenttham085](https://clawhub.ai/user/nguyenttham085)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for server health status, including uptime, load averages, RAM, swap, and root disk usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends host resource data to a fixed external webhook on every run.

Mitigation: Remove the hardcoded webhook POST or make remote monitoring explicit, user-controlled, opt-in, and documented with the destination and fields sent.

Risk: Host resource data can expose operational details about the machine where the skill runs.

Mitigation: Use only on approved machines and review the output destination before running in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nguyenttham085/skills/test-monitor-openclaw-server)
- [Publisher Profile](https://clawhub.ai/user/nguyenttham085)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text server health report with agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local uptime, load, memory, swap, and root disk usage.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
