## Description:

Read, summarize, propose edits, and write back changes to Markdown todo files using line-stable bot markers without altering task identity or completing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitsujy](https://clawhub.ai/user/nitsujy)

### License/Terms of Use:


## Use Case:

Developers and todo-list users use this skill to review todolist-md Markdown files, generate summaries or suggested tasks, and write human-reviewable outcomes back with bot comment markers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google Drive access may expose or modify Markdown files beyond the intended todo workflow.

Mitigation: Use a dedicated Google account or reduced OAuth scope where possible, and keep sensitive Markdown files outside reviewed folders.

Risk: Under-scoped write-back behavior could add suggestions to files that were not meant to be AI-reviewed.

Mitigation: Enable per-file opt-in controls, validate target files before apply mode, and review every suggestions JSON before writing changes.

Risk: Generated suggestions may be incorrect or may change task meaning if applied without review.

Mitigation: Keep suggestions in bot-marked sections, use dry runs for review, and require explicit user confirmation before completing tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nitsujy/skills/todolist-md-clawdbot-copy)
- [todolist-md project homepage](https://github.com/NitsujY/todolist-md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON request or suggestion files, and shell commands for helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes only bot-marked Markdown suggestions or review metadata when configured, and prepares compact task extracts for separate agent processing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
