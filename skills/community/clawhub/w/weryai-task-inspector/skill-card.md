## Description:

Inspects existing WeryAI task IDs and batch IDs, summarizes task status, surfaces podcast content_status, and extracts available output artifacts through read-only query endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check the state of existing WeryAI generation tasks or batches, debug stuck jobs, and collect returned image, video, audio, lyrics, cover, or script artifacts without submitting new work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom WERYAI_BASE_URL could redirect authenticated requests and expose the WERYAI_API_KEY.

Mitigation: Run the skill only in environments where WERYAI_BASE_URL is unset or controlled by trusted administrators.

Risk: The package includes account balance lookup code outside the documented task-inspection workflow.

Mitigation: Review installed files before use and limit execution to the documented task-inspector entry point for task or batch status checks.

## Reference(s):

- [WeryAI Task Query APIs](references/tasks-api.md)
- [Query Task Details](https://docs.weryai.com/api-reference/tasks/query-task-details)
- [Query Batch Task Status](https://docs.weryai.com/api-reference/tasks/query-batch-task-status)
- [ClawHub skill page](https://clawhub.ai/weryai-developer/skills/weryai-task-inspector)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON from the inspector command, usually summarized to the user in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes normalized phase and status, optional contentStatus, extracted artifacts, raw task payloads, and structured error codes.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
