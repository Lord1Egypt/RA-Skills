## Description:

Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma (vector) + ripgrep (keyword).

This skill is ready for commercial/non-commercial use.

## Publisher:

[virajsanghvi1](https://clawhub.ai/user/virajsanghvi1)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use RAGLite to distill local or private documents into auditable Markdown, index them with Chroma and ripgrep, and query that local cache for repeated retrieval tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or confidential documents may be processed by an engine whose locality and retention behavior are not clear.

Mitigation: Use an explicitly understood --engine value and avoid medical, internal, or confidential documents until engine handling is confirmed.

Risk: Setup installs mutable Python packages and can use a custom package index.

Mitigation: Install in an isolated environment and set RAGLITE_PIP_INDEX_URL only for a fully trusted package index.

Risk: Third-party source documents may contain prompt injection attempts.

Mitigation: Treat source text as untrusted data and review distilled Markdown and retrieval outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/virajsanghvi1/skills/raglite)
- [Project repository listed in artifact](https://github.com/VirajSanghvi1/raglite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces distilled Markdown artifacts, local index/query workflows, and retrieval responses through the raglite CLI.]

## Skill Version(s):

1.0.8 (source: frontmatter, manifest.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
