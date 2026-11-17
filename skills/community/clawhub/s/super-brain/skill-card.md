## Description:

AI self-enhancement system that gives an agent persistent cross-session memory for user preferences, conversation history, service patterns, projects, reminders, and personalized assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aboutyao](https://clawhub.ai/user/aboutyao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add persistent local memory to an agent so it can remember user preferences, track ongoing work, summarize conversations, learn response patterns, and raise follow-up reminders across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes startup behavior and encourages automatic memory activation across sessions.

Mitigation: Review and disable startup injection unless persistent memory is intentionally desired.

Risk: The skill stores broad personal conversation data, including profiles, preferences, moods, projects, reminders, and agent activity.

Mitigation: Make storage opt-in, redact sensitive content before writes, and avoid saving raw conversations or secrets.

Risk: Shared memory access by subagents can expose more personal context than a subtask requires.

Mitigation: Limit subagent access to the minimum required data and avoid mounting the full memory database.

Risk: Deletion, export, and encryption controls are described but may need hardening before sensitive or shared-machine use.

Mitigation: Add verified delete, export, retention, and encryption workflows before using the skill with sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aboutyao/skills/super-brain)
- [Design](artifact/DESIGN.md)
- [Workflow](artifact/references/workflow.md)
- [Database schema](artifact/references/schema.sql)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite, ChromaDB, cache, and startup-checklist files when its scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
