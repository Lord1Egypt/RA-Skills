## Description: <br>
Smart Cache provides a local intelligent cache for AI assistants, using exact and semantic matching to reduce repeated API calls and speed responses to similar requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heimaomao83](https://clawhub.ai/user/heimaomao83) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add and manage a local cache layer for AI assistant prompts and responses, including exact-match cache hits, semantic cache lookup, cache cleanup, cost tracking, and MCP integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and responses may be retained in the local cache. <br>
Mitigation: Install only where local retention is acceptable, configure TTL and cleanup policies, and avoid caching secrets, customer data, proprietary content, or regulated information. <br>
Risk: Semantic embedding can send prompt text to external embedding providers. <br>
Mitigation: Use a local embedding provider or disable semantic embedding when prompts may contain sensitive content. <br>
Risk: HTTP MCP mode can expose unauthenticated cache read, write, or delete operations if bound to a public or shared interface. <br>
Mitigation: Prefer stdio mode; if HTTP mode is needed, bind it to localhost and protect access with external controls. <br>


## Reference(s): <br>
- [Smart Cache API Reference](references/api_reference.md) <br>
- [Smart Cache ClawHub Page](https://clawhub.ai/heimaomao83/sunlixue-smart-cache) <br>
- [OpenAI Embeddings API](https://api.openai.com/v1/embeddings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, JSON configuration examples, Python code examples, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local cache configuration and embedding provider credentials for semantic caching.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
