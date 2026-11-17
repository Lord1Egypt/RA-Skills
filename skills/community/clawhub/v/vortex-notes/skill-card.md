## Description:

Read, search, and write the user's Vortex Notes vault -- plain-markdown notes with local semantic search, daily notes, and durable facts with supersession.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vortex-303](https://clawhub.ai/user/vortex-303)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to search, read, and update a local Vortex Notes markdown vault for note capture, daily journaling, durable memory, and retrieving prior knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently read and modify notes in the configured Vortex Notes vault through an external npm tool.

Mitigation: Install only if the vortex-notes npm package is trusted, prefer read-only mode for searches, and require explicit note-related requests before writes.

Risk: Sensitive information stored in the notes vault may be exposed to agents using the skill.

Mitigation: Avoid storing highly sensitive secrets in the vault unless the local environment and access controls are appropriate.

## Reference(s):

- [Vortex Notes ClawHub skill page](https://clawhub.ai/vortex-303/skills/vortex-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and note-content conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or edit markdown notes in the configured vault when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
