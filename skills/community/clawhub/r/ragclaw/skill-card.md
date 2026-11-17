## Description:

Local-first knowledge base to index, search, and manage documents and web pages offline using SQLite and local embedding models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emdzej](https://clawhub.ai/user/emdzej)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build and query a local knowledge base from selected files, directories, URLs, images, PDFs, and code. It supports offline document retrieval, reindexing, source management, embedder management, and knowledge-base maintenance through the RagClaw CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned globally installed third-party ragclaw CLI resolved from PATH.

Mitigation: Install only from a trusted publisher, prefer an exact pinned CLI version, and review which executable RAGCLAW_BIN or PATH resolves before use.

Risk: Broad indexing commands can ingest local directories, URLs, images, PDFs, and code into persistent local databases.

Mitigation: Use explicit /kb commands with narrow include and exclude patterns, max-depth, and max-files settings before indexing private material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emdzej/skills/ragclaw)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text; optional machine-readable JSON for search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local SQLite knowledge-base files and local configuration when RagClaw commands are executed.]

## Skill Version(s):

0.5.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
