## Description:

Document intelligence pipeline with visual search, OCR, and field capture

This skill is ready for commercial/non-commercial use.

## Publisher:

[curtisgc1](https://clawhub.ai/user/curtisgc1)

### License/Terms of Use:

MIT

## Use Case:

External users, field service teams, researchers, mechanics, and developers use this skill to ingest document collections, search them with text and visual retrieval, identify parts from images, and capture field notes for future retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes an unverified remote installer command.

Mitigation: Review the installer before execution and prefer a pinned or package-manager-based Ollama installation path.

Risk: The skill handles broad document and image collections that may include sensitive or regulated content.

Mitigation: Classify documents before ingestion, limit indexed sources to approved collections, and confirm retention and access controls for the local knowledge base.

Risk: Configured cloud, web-search, Telegram, or email integrations may receive queries, OCR text, document context, or images.

Mitigation: Use local-only mode for confidential collections and enable external providers only after data-sharing and provider approvals are complete.

## Reference(s):

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Ollama](https://ollama.ai)
- [OpenRouter](https://openrouter.ai)
- [Brave Search API](https://brave.com/search/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP tool guidance and structured examples for search, ingestion, field note capture, image identification, status checks, and client configuration.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
