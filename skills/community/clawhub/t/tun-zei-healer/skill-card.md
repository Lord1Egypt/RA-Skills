## Description:

吞贼·净化魄 is an auto-healing skill for diagnosing system instability, proposing recovery actions, cleaning redundant files, and applying resilience patterns such as retries, rollback, and circuit breakers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent inspect system health, report detected issues, recommend recovery actions, and perform constrained remediation such as retries, rollback planning, redundancy cleanup, or process recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt agents to delete redundant files, roll back state, restart processes, or trigger recovery actions without enough limits or confirmation.

Mitigation: Use read-only diagnosis by default, require exact target lists and user confirmation before changes, keep backups for rollback, and restrict filesystem or process access to explicit allowlists.

Risk: Automated recovery recommendations can affect production stability if applied broadly or without review.

Mitigation: Run in constrained workspaces or non-production environments unless the agent is required to ask before executing changes, and review proposed actions before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown diagnostic reports with optional command or remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health status, issue severity, executed repairs, and follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
