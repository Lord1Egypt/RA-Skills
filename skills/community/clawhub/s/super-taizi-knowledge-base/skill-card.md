## Description:

Super Taizi Knowledge Base helps an agent store, search, and manage a personal knowledge base using vector search, entity relationships, and notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent add text or files to a personal OpenClaw knowledge base, search stored knowledge, view statistics, and create notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unbundled local Python script at the documented path.

Mitigation: Install only after verifying the local vector_kb.py script source and integrity, and prefer a release that bundles or hashes the script.

Risk: The skill can persist user text, files, notes, and extracted relationships in local OpenClaw storage.

Mitigation: Use it only with content approved for local retention, review the documented storage directories, and document how to inspect or delete stored data.

Risk: The security evidence notes weak scoping and consent controls around automatic knowledge-base writes.

Mitigation: Ask for explicit user confirmation before add or add-file actions and limit writes to the intended knowledge, memory, and notes directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-taizi-knowledge-base)
- [ClawHub publisher profile](https://clawhub.ai/user/subaru0573)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local file paths and persistent storage locations.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
