## Description:

Monitor session context levels and proactively save checkpoints before compaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbillwatsonx](https://clawhub.ai/user/xbillwatsonx)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to monitor long-running session context, warn before compaction, and preserve key decisions, pending tasks, modified files, and unresolved issues in local checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write durable session summaries to local memory, which may preserve secrets, personal data, or raw external instructions if used without review.

Mitigation: Review each checkpoint before storage, omit sensitive data and raw external instructions, and limit when memory writes occur.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown guidance with inline shell commands and checkpoint templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory checkpoint content that should be reviewed before durable storage.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
