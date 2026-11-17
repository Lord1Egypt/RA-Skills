## Description:

Fast semantic search for AI agent memory files using TF-IDF and SQLite, enabling context retrieval from MEMORY.md or markdown documentation without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mig6671](https://clawhub.ai/user/mig6671)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to index markdown memory or documentation files and retrieve the most relevant sections before a task. It is aimed at lightweight, local context search where shell commands, configuration edits, and textual search results are useful to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create a persistent plaintext SQLite copy of sensitive memory or operational notes.

Mitigation: Index only non-secret memory or documentation, or add redaction, owner-only file permissions, and explicit opt-in scope before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mig6671/skills/vector-memory-hack)
- [Artifact README](artifact/README.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, plain text search results, and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include ranked section titles, similarity scores, and truncated section content.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
