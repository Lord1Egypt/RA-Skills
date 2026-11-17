## Description:

Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

Developers and engineers use Qmd to index local project or documentation folders and retrieve relevant file content through BM25, vector, hybrid search, and MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata references an unpinned GitHub package, creating supply-chain risk.

Mitigation: Install from a reviewed release or pinned commit when available.

Risk: Indexed collection contents are cached locally and become searchable.

Mitigation: Add only directories whose contents are intended to be indexed, searched, and stored in the local qmd cache.

## Reference(s):

- [Qmd ClawHub Skill Page](https://clawhub.ai/steipete/skills/qmd)
- [qmd GitHub package](https://github.com/tobi/qmd)
- [Publisher homepage](https://tobi.lutke.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include qmd commands for indexing, status checks, search, document retrieval, and MCP mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
