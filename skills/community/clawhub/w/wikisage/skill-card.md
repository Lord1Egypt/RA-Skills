## Description:

A Karpathy-style persistent LLM wiki for ingesting sources into a local markdown knowledge base, querying long-lived local knowledge first, and linting wiki health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harryzsh](https://clawhub.ai/user/harryzsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill-aware agent users use Wikisage to maintain a persistent private markdown wiki, ingest source material with deduplication, answer questions from local knowledge, and run wiki health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local wiki may store private client, account, or decision history data.

Mitigation: Keep WIKI_ROOT private and use a scoped filesystem MCP server that limits reads and writes to the intended wiki directory.

Risk: Fallback read, write, edit, or shell search paths can operate outside the intended wiki boundary if used carelessly.

Mitigation: Prefer the Obsidian filesystem MCP channel and avoid shell fallback for untrusted input.

Risk: Ingesting untrusted URLs can fetch and persist content without strong network controls.

Mitigation: Do not ingest untrusted URLs unless network access and source trust have been reviewed.

Risk: The optional embedding workflow can send wiki content to AWS Bedrock and OpenSearch.

Mitigation: Skip embed.py unless external processing is intended and the AWS account, secret, and OpenSearch index are constrained for the data.

## Reference(s):

- [ClawHub Wikisage skill page](https://clawhub.ai/harryzsh/skills/wikisage)
- [Wikisage project repository](https://github.com/harryzsh/wikisage)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw AgentSkill repository](https://github.com/openclaw/openclaw)
- [mcporter](https://github.com/CrazyPython/mcporter)
- [Model Context Protocol filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text answers with command snippets and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local markdown wiki pages, indexes, logs, deduplication caches, and lint reports under WIKI_ROOT; optional embedding workflow can send wiki content to AWS Bedrock and OpenSearch.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
