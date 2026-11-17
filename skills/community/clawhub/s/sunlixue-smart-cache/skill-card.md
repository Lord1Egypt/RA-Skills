## Description:

Smart Cache provides a local exact and semantic cache for AI assistant prompts to reduce repeated API calls and speed up responses to similar requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heimaomao83](https://clawhub.ai/user/heimaomao83)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add local L1 exact-match and L2 semantic caching around AI assistant requests, including CLI, Python API, and MCP server workflows. It is intended to reduce repeated model calls, improve response latency, and track estimated token and cost savings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cached prompts and responses may include private prompts, secrets, or regulated data stored on the local filesystem.

Mitigation: Use local-only storage where possible, avoid caching sensitive prompts, and clear or limit cached data according to the data handling requirements for the environment.

Risk: HTTP MCP mode can expose cached data or API-key-backed functionality if it is made reachable beyond localhost without authentication.

Mitigation: Keep HTTP mode bound to localhost unless a separate authenticated network boundary is provided.

Risk: Embedding provider configuration can mix API keys across providers, including a path where the OpenAI provider may reuse a DashScope key.

Mitigation: Configure provider-specific API keys explicitly and review environment variables and config files before enabling network embedding providers.

## Reference(s):

- [Smart Cache API Reference](artifact/references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/heimaomao83/skills/sunlixue-smart-cache)
- [OpenAI Embeddings API Endpoint](https://api.openai.com/v1/embeddings)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, Python snippets, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local cache files, SQLite entries, MCP tool responses, and embedding-provider configuration.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
