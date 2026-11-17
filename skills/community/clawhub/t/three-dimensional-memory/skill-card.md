## Description:

Helps AI assistants maintain local memory across daily timeline logs, conversation backups, and topic-based project folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amlyx](https://clawhub.ai/user/amlyx)

### License/Terms of Use:

MIT

## Use Case:

Users and AI assistants use this skill to create and maintain workspace memory organized by date, conversation, and topic so prior work, decisions, and context can be retrieved later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory may preserve full conversation transcripts, preferences, or sensitive context.

Mitigation: Prefer summaries over full transcripts, exclude secrets and sensitive personal or business data, restrict file access, and use a deletion or retention routine.

Risk: Memory folders may be accidentally committed, synced, or exposed.

Mitigation: Avoid committing or syncing memory folders and keep them outside shared repositories or add ignore rules before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amlyx/skills/three-dimensional-memory)
- [Artifact skill overview](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, directory structures, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local memory directories and Markdown records when followed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
