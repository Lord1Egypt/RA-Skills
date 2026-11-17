## Description:

qmd Search helps agents use the qmd CLI for fast local keyword, semantic, and reranked search across markdown files, notes, docs, and indexed collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bheemreddy181](https://clawhub.ai/user/bheemreddy181)

### License/Terms of Use:


## Use Case:

Developers and agents use qmd Search to discover files, search local markdown and code collections, retrieve snippets or full files, and gather context before answering questions or making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private notes or source code can become part of a local qmd index when broad folders are added as collections.

Mitigation: Add only intended folders as collections and review collection scope before running qmd update.

Risk: Embedding or reranking workflows may download local models and use local storage or compute.

Mitigation: Enable vector search only when needed and plan for local model downloads before running qmd embed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bheemreddy181/skills/qmd-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include qmd search commands, collection-management commands, file paths, snippets, or instructions for retrieving full files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
