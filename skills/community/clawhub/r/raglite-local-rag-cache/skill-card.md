## Description:

Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma + hybrid search (vector + keyword).

This skill is ready for commercial/non-commercial use.

## Publisher:

[virajsanghvi1](https://clawhub.ai/user/virajsanghvi1)

### License/Terms of Use:


## Use Case:

Developers and agents use RAGLite to condense private or local documents into structured Markdown, index them in a local Chroma collection, and query them with hybrid vector and keyword retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer retrieves changing code from GitHub main, so the installed behavior can change between releases or installs.

Mitigation: Review the dependency before installation and prefer a pinned, reviewed raglite commit or release.

Risk: The skill is intended for private or sensitive documents and sends condensation work through the configured OpenClaw gateway and stores retrieval data in Chroma.

Mitigation: Use only trusted local or approved endpoints, and confirm where the Chroma database is stored before processing sensitive documents.

## Reference(s):

- [ClawHub RAGLite skill listing](https://clawhub.ai/virajsanghvi1/skills/raglite-local-rag-cache)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown files and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes distilled Markdown outputs, optional node and index files, and .raglite metadata under the configured output directory.]

## Skill Version(s):

1.0.0 (source: evidence release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
