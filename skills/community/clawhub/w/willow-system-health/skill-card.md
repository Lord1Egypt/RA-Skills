## Description:

Audit the Willow local AI stack for subsystem failures, drift, and resource bloat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check Willow local AI stack health, diagnose slow or broken sessions, verify Postgres, Ollama, and MCP availability, inspect worktrees and tasks, and run deeper daily or weekly diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks a local Willow stack and exposes default local Postgres credential handling.

Mitigation: Use it only on a Willow local AI stack you control and review the default Postgres DSN before installing in shared or production-like environments.

Risk: Suggested cleanup actions can remove worktrees or models or run Postgres VACUUM.

Mitigation: Show the exact change first and require explicit user confirmation before deleting worktrees, removing models, or running VACUUM.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rudi193-cmd/skills/willow-system-health)
- [Publisher Profile](https://clawhub.ai/user/rudi193-cmd)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands and optional JSON diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports HEALTHY, WARN, CRITICAL, or SKIP status per subsystem and requires confirmation before cleanup actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
