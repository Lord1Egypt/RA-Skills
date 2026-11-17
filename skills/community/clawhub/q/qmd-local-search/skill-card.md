## Description:

Fast local search for markdown files, notes, and docs using qmd CLI, combining BM25 full-text search, vector semantic search, and LLM reranking locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bheemreddy181](https://clawhub.ai/user/bheemreddy181)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search indexed local markdown files, notes, documentation, and code-related content, then retrieve relevant snippets or files for context gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local indexes may include sensitive files if broad directories are added as qmd collections.

Mitigation: Keep collections scoped and avoid indexing sensitive directories unless that access is intended.

Risk: Embedding or reranking setup may create local indexes and download local model files.

Mitigation: Run qmd setup and embedding commands only in environments where local index and model storage are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bheemreddy181/skills/qmd-local-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include qmd commands, result-format guidance, collection-scoping advice, and file retrieval suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
