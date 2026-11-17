## Description:

Produces a self-contained handoff prompt for running planned work in a fresh sub-agent-enabled session with explicit task decomposition and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn planned or discussed work into a paste-ready orchestrator prompt for a fresh session that dispatches sub-agents and requires concrete verification for each task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated handoff prompt can send a follow-on session into incorrect paths, tasks, or verification commands.

Mitigation: Review the exact paths, task list, verification commands, and final integration check before using the prompt in a sub-agent-enabled session.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown fenced prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes absolute paths, task list, verification contract, final integration check, and failure-handling policy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
