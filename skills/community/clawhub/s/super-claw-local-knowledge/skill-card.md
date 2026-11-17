## Description:

Super Claw Local Knowledge helps an agent convert uploaded DOCX, PDF, XLSX, and PPTX documents into a local Markdown knowledge base and retrieve relevant stored content for future responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add uploaded documents to an OpenClaw local knowledge base, then retrieve relevant indexed Markdown content when answering questions that depend on stored documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded documents may be converted, stored, indexed, and reused from the local OpenClaw workspace.

Mitigation: Install only when local document persistence is intended, review the knowledge base index and stored Markdown files, and avoid adding sensitive documents unless reuse is acceptable.

Risk: The optional SOUL.md change can make the agent proactively retrieve stored knowledge across future sessions.

Mitigation: Add the SOUL.md retrieval block only when persistent proactive retrieval is desired, and remove it if retrieval should remain user-initiated.

Risk: The ingestion workflow recommends deleting uploaded source files after successful conversion and indexing.

Mitigation: Keep backups of original files before ingestion and confirm converted Markdown quality before deleting source documents.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/subaru0573/skills/super-claw-local-knowledge)
- [Document ingestion workflow](artifact/references/add_knowledge.md)
- [Knowledge retrieval workflow](artifact/references/retrieval_knowledge.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON index entries, and file path instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace files under .openclaw/workspace/memory/knowledge_base and updates knowledge_base_index.json when ingestion is performed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
