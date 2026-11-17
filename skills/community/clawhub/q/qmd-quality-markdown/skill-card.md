## Description:

Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonnenberglauramarie-afk](https://clawhub.ai/user/sonnenberglauramarie-afk)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to install and operate qmd for indexing local Markdown or documentation collections and searching them with BM25, vector, or hybrid queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs qmd from an unpinned GitHub source, so future upstream changes can alter installed behavior.

Mitigation: Review the referenced project before installation and use a pinned or audited package source where the deployment process supports it.

Risk: Local indexes may include sensitive files if broad directories are added.

Mitigation: Index only intended directories, exclude sensitive paths, and manage cached index data under ~/.cache/qmd according to local data-handling policy.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sonnenberglauramarie-afk/skills/qmd-quality-markdown)
- [qmd install package](https://github.com/tobi/qmd)
- [Publisher homepage](https://tobi.lutke.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local qmd indexes and Ollama-backed embedding or reranking behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
