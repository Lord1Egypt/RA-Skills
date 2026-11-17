## Description:

Submits complex QClaw user requests to a WorkBuddy task queue for document generation, data analysis, batch file processing, scheduled automation, and other multi-step work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

QClaw users and operators use this skill to hand off complex or long-running requests to WorkBuddy when the task requires document creation, file processing, deeper analysis, or automation beyond a simple conversational response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad user requests can be routed into immediate external or local WorkBuddy automation without clear confirmation.

Mitigation: Require explicit confirmation before submitting tasks involving files, private data, batch changes, scheduled work, or document generation.

Risk: The documented queue-command pattern could be implemented with unsafe shell-string interpolation.

Mitigation: Call the queue script with structured arguments and avoid constructing shell commands directly from user input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuboacean/skills/qclaw-task-submitter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and task-status response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a task description, task ID, status query, or result retrieval command for WorkBuddy.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
