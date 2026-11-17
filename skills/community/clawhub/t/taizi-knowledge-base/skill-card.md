## Description:

A personal knowledge-base skill for storing, searching, and organizing notes with vector retrieval and entity relationship management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangepier-crypto](https://clawhub.ai/user/tangepier-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to store knowledge, add note files, search indexed content, and review knowledge-base statistics in a local personal knowledge workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and index local user content, including note files, which may accidentally include sensitive information.

Mitigation: Use it only for approved personal knowledge content, avoid secrets or private files, and require explicit confirmation before storage or add-file actions.

Risk: Shell-style commands for text and file operations can be unsafe if arguments are interpolated directly.

Mitigation: Run commands through a safe wrapper that passes arguments without shell interpolation and limits file indexing to approved directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangepier-crypto/skills/taizi-knowledge-base)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist indexed content and notes in local OpenClaw knowledge, ontology, and notes directories when storage actions are used.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
