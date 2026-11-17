## Description:

Task Tracker Pro helps an agent break multi-step work into local Markdown task files, update progress as steps complete, resume interrupted sessions, and coordinate multi-agent task ownership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yurio99](https://clawhub.ai/user/yurio99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to keep multi-step agent work visible and resumable by recording plans, progress, owners, blockers, checks, and execution logs in local Markdown task files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task names, steps, logs, and progress are persisted under ~/.openclaw/workspace/tasks/ and may contain sensitive working details.

Mitigation: Avoid putting secrets or sensitive details in tracked task text, and review local task files before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yurio99/skills/task-tracker-pro)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown task files with checklist items, execution logs, and brief user-facing status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists progress in local task files under ~/.openclaw/workspace/tasks/.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
