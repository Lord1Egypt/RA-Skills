## Description:

Local-first RAG cache: distill docs into structured Markdown, then index/query with Chroma + hybrid search (vector + keyword).

This skill is ready for commercial/non-commercial use.

## Publisher:

[virajsanghvi1](https://clawhub.ai/user/virajsanghvi1)

### License/Terms of Use:


## Use Case:

Developers and engineers use RAGLite to condense local or private documents into structured Markdown, index them in Chroma, and query them with hybrid vector and keyword retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install script installs RAGLite from a mutable remote GitHub main branch.

Mitigation: Review the upstream RAGLite repository and pin installation to a trusted commit or release before deployment.

Risk: The default OpenClaw condensation engine may send processed document contents to the configured gateway.

Mitigation: Use the skill only with a trusted gateway and avoid sensitive personal, medical, or internal documents unless gateway logging and retention behavior are acceptable.

## Reference(s):

- [RAGLite ClawHub listing](https://clawhub.ai/virajsanghvi1/skills/virajsanghvi1-raglite)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance for running RAGLite, plus generated Markdown document summaries, indexes, metadata, run statistics, and query results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+, pip, a reachable Chroma server for indexing and querying, and ripgrep for keyword search.]

## Skill Version(s):

1.0.0 (source: frontmatter, OpenClaw plugin manifest, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
