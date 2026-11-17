## Description:

Read OpenClaw policy values from PostgreSQL through the local Supabase Docker stack for inspecting keys such as auto_approve, priority_routing, or available_skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecosincronia](https://clawhub.ai/user/ecosincronia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw policy keys and read policy values from a local Supabase PostgreSQL database during operational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw policy configuration that may contain sensitive operational information.

Mitigation: Install and run it only where an agent is permitted to inspect OpenClaw policy data.

Risk: The script requires Docker access to the local Supabase database container, which is a meaningful local privilege.

Mitigation: Restrict execution to trusted environments and review commands before running them against the local Docker stack.

## Reference(s):

- [Read Policy on ClawHub](https://clawhub.ai/ecosincronia/skills/read-policy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text or pretty-printed JSON returned by shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the local OpenClaw policy rows available in the Supabase PostgreSQL database.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
