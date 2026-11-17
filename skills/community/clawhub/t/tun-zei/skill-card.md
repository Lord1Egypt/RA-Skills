## Description:

Tun Zei provides error diagnosis suggestions, simulated cleanup reporting, and local system health checks for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect common runtime errors, get suggested fixes, check local system health, and produce cleanup reports before deciding on manual remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup behavior may be mistaken for actual file deletion even though the current evidence indicates simulated removal.

Mitigation: Treat cleanup output as a report, and verify behavior in a controlled environment before relying on it for real cleanup.

Risk: Fix suggestions may be incomplete for complex runtime failures.

Mitigation: Review suggested fixes manually and test changes before applying them to production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lt8899789/skills/tun-zei)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON objects and concise diagnostic text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cleanup results are reports or simulations; verify behavior before relying on them for actual deletion or remediation.]

## Skill Version(s):

1.0.35 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
