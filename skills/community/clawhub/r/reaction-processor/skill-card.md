## Description:

Record real OpenClaw events and reactions for the current closed-loop workflow, including duplicate-skipped and proposal-created stale mission outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecosincronia](https://clawhub.ai/user/ecosincronia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to record OpenClaw closed-loop stale mission outcomes in event and reaction tables, and to update trigger fire metadata when a proposal is created.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent event, reaction, and trigger metadata using administrative database access.

Mitigation: Use it only in a trusted local OpenClaw/Supabase environment where the caller is allowed to make these writes.

Risk: Weak scoping and validation could record unverified workflow outcomes.

Mitigation: Prefer a narrower database role or reviewed stored procedure, require explicit confirmation before writes, and validate that the recorded outcome matches the verified workflow state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ecosincronia/skills/reaction-processor)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands write persistent OpenClaw audit, reaction, and trigger metadata in a trusted local Supabase database.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
