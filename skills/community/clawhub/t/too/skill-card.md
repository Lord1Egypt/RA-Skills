## Description:

A skill for managing todo lists, including creating, updating, deleting, and organizing tasks with priorities and deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, update, delete, list, and organize todo items with priorities, deadlines, categories, and status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Todo data storage, retention, and access controls are undefined if users pair the skill with files, tools, or external services.

Mitigation: Define where todo data is stored, who can access it, and how updates are logged before using the skill with persistent tools.

Risk: Ambiguous natural-language update or delete requests could target the wrong task.

Mitigation: Ask for confirmation or use stable task identifiers before changing or removing existing todo items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/too)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with task examples and a structured todo schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, tool use, or persistent storage is defined by the artifact.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
