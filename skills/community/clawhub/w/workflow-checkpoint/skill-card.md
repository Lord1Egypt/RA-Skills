## Description:

Workflow Checkpoint helps agents save progress and recover from any point in multi-step AI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to checkpoint multi-step AI workflows, record progress and artifacts, and resume from the last verified step after failures or interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint files may persist secrets, credentials, private customer data, sensitive outputs, or internal host details.

Mitigation: Do not checkpoint sensitive data, and periodically delete old files under memory/checkpoints.

Risk: A resumed workflow may rely on stale or missing artifacts from earlier steps.

Mitigation: Verify saved artifacts still exist before skipping completed steps during recovery.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON checkpoint file examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local checkpoint records under memory/checkpoints when applied by an agent.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
