## Description:

Personal execution engine for tasks, projects, reminders, commitments, follow-ups, and next actions that captures natural language, structures action items, tracks momentum, and surfaces a human-friendly next step using local-only storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticio](https://clawhub.ai/user/agenticio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to capture tasks, commitments, reminders, and follow-ups, then choose a next action based on urgency, energy, time, and task freshness. It is suited for local personal productivity workflows where todo data should remain in the OpenClaw workspace memory directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores task, archive, and stats data in local JSON files under the OpenClaw workspace memory directory.

Mitigation: Install it only for workflows where local todo storage is expected, and avoid entering sensitive task details unless the local workspace storage is appropriate for that data.

Risk: The skill may activate on broad task-planning or reminder language.

Mitigation: Review agent invocations when discussing planning, commitments, reminders, or follow-ups, and disable or remove the skill if it triggers outside the intended workflow.

Risk: Local file updates can corrupt todo state if interrupted or if temporary-file handling fails.

Mitigation: Keep backups of important todo data and prefer updates through the bundled scripts until the publisher hardens the file-write behavior.

## Reference(s):

- [Todo Philosophy](references/philosophy.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance with shell command examples and script-generated text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON todo, archive, and stats files under ~/.openclaw/workspace/memory/todo.]

## Skill Version(s):

3.0.1 (source: skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
