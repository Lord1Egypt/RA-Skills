## Description:

Guide AI to create NocoBase workflows - triggers, conditions, data operations, SQL, and scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander-lq](https://clawhub.ai/user/alexander-lq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through planning, creating, enabling, and verifying NocoBase workflows for data-change triggers, schedules, conditional branches, SQL nodes, updates, queries, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw SQL workflow nodes can modify live business data if generated or enabled without review.

Mitigation: Require explicit human confirmation before running SQL or enabling SQL-backed workflows, prefer higher-level update nodes or parameterized SQL, and test in a non-production NocoBase environment first.

Risk: Bulk deletion by prefix can remove workflows that the user did not intend to delete.

Mitigation: Preview matched workflows with listing or inspection tools before deletion and require explicit confirmation of the exact prefix and affected workflow names.

Risk: Automatically enabled workflows can trigger repeated or unintended data changes.

Mitigation: Create all nodes before enabling, inspect the workflow definition, and verify trigger conditions, target collections, and idempotency before activation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexander-lq/skills/work-fllows)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline command, JSON, and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing instructions for constructing NocoBase workflow definitions and tool calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
