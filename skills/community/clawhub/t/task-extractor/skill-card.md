## Description:

Extract, track, and verify completion of multiple tasks from a single user message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decompose compound user messages into a tracked task queue, execute items in dependency order, and report per-item completion evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may aggressively convert compound or ambiguous prompts into executable task queues and execute more than intended.

Mitigation: Use it only where that behavior is desired, and review the extracted checklist before allowing broad execution.

Risk: The skill can persist task details locally in TASK_QUEUE.md.

Mitigation: Avoid using it on prompts containing secrets, personal data, or quoted instructions intended only for analysis, and delete TASK_QUEUE.md when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dodge1218/skills/task-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task queue and checklist-style status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update TASK_QUEUE.md in the workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
