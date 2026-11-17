## Description:

Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma + hybrid search (vector + keyword).

This skill is ready for commercial/non-commercial use.

## Publisher:

[virajsanghvi1](https://clawhub.ai/user/virajsanghvi1)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to build a local, auditable RAG library from documents they need to query repeatedly, including private notes, school work, medical records, and internal runbooks. It condenses source documents to Markdown, indexes them in Chroma, and supports hybrid vector and keyword retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches live code from an unpinned GitHub main branch.

Mitigation: Prefer a version that pins RAGLite to a reviewed commit or release before installing in production or with sensitive data.

Risk: The skill may process private, medical, personal, school, or internal business documents through the default OpenClaw condensation engine.

Mitigation: Confirm whether OpenClaw sends document contents to a local gateway, private network service, or external provider before indexing sensitive files.

Risk: The security verdict is suspicious because installation and document processing require review before use.

Mitigation: Review the skill, install path, dependencies, Chroma endpoint, and OpenClaw gateway configuration before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/virajsanghvi1/skills/raglite-library)
- [ClawHub publisher profile](https://clawhub.ai/user/virajsanghvi1)
- [RAGLite install target referenced by artifact](https://github.com/VirajSanghvi1/raglite.git@main)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; runtime commands may write Markdown outputs and .raglite metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented runtime writes *.tool-summary.md, *.execution-notes.md, optional outlines and node Markdown files, per-document index files, a root index.md, and .raglite cache, stats, and error metadata.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter; artifact manifest and plugin declare 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
