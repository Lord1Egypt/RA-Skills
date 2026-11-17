## Description:

Qclaw Result Checker helps an agent check WorkBuddy task status and retrieve completed task results through QClaw queue commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent whether WorkBuddy tasks have completed, list queue status, and retrieve completed task summaries or full results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal prior WorkBuddy task content, result details, and local paths in the current chat.

Mitigation: Narrow activation to explicit QClaw or WorkBuddy result requests, require a task ID or confirmation before showing full results, and redact file paths by default.

Risk: The skill uses a shell command pattern that accepts a task ID supplied by the user.

Mitigation: Validate task IDs against the local queue before running result commands and avoid passing untrusted free-form text as the task ID.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuboacean/skills/qclaw-result-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and task result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WorkBuddy task IDs, task descriptions, result details, status, and local file paths when returned by the queue command.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
