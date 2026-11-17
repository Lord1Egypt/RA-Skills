## Description:

Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sambiner](https://clawhub.ai/user/sambiner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to index local files, search them with BM25, vector, or hybrid retrieval, and inspect matching documents through qmd commands or MCP mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The qmd dependency is installed from an unpinned GitHub source.

Mitigation: Prefer a pinned or reviewed qmd revision when stronger supply-chain control is required.

Risk: Indexed file contents may be stored locally under ~/.cache/qmd.

Mitigation: Index only directories intended to be searchable and review local cache handling before use with sensitive files.

## Reference(s):

- [qmd install package](https://github.com/tobi/qmd)
- [Qmd2 on ClawHub](https://clawhub.ai/sambiner/skills/qmd2)
- [sambiner publisher profile](https://clawhub.ai/user/sambiner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local qmd indexing, search, retrieval, and MCP usage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
