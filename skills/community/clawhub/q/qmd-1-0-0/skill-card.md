## Description:

Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[instant-picture](https://clawhub.ai/user/instant-picture)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to install and operate qmd for local file indexing, collection management, keyword search, vector search, hybrid reranked search, document retrieval, and MCP mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs qmd from an unpinned GitHub repository, which creates supply-chain exposure if the upstream changes unexpectedly.

Mitigation: Use a reviewed or pinned qmd revision where possible and install only when the upstream repository is trusted.

Risk: Indexing sensitive directories can make their contents searchable in the local qmd cache.

Mitigation: Avoid indexing sensitive paths unless that searchability is intended, and review collection masks before running indexing commands.

Risk: Running qmd with elevated privileges could expand access to files and cache contents beyond the intended user scope.

Mitigation: Run qmd with normal user privileges and keep the default local cache access scoped to the intended user.

## Reference(s):

- [qmd upstream repository](https://github.com/tobi/qmd)
- [qmd homepage](https://tobi.lutke.com)
- [ClawHub skill page](https://clawhub.ai/instant-picture/skills/qmd-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference local filesystem paths, qmd commands, Ollama configuration, and MCP mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
