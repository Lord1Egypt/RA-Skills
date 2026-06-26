## Description: <br>
Use Ragora MCP tools and REST API to discover, search, and synthesize answers from knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mregmi](https://clawhub.ai/user/mregmi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to connect MCP-compatible or HTTP-capable agents to Ragora knowledge bases for grounded search, source-backed summaries, cross-collection comparisons, due diligence, and verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent sends user queries and retrieved context to Ragora-backed collections using a live API key. <br>
Mitigation: Confirm the intended Ragora account and collections before use, and avoid sending sensitive private data unless Ragora is approved for that data. <br>
Risk: A leaked or hardcoded RAGORA_API_KEY could expose account access or billing usage. <br>
Mitigation: Store RAGORA_API_KEY in an environment variable or secret manager and mask keys in logs, configuration examples, and final responses. <br>
Risk: Marketplace retrievals may consume credits or fail when the account lacks access. <br>
Mitigation: Check balance and collection access when billing or permission errors occur, and report credit constraints before continuing retrieval-heavy workflows. <br>


## Reference(s): <br>
- [Ragora OpenClaw repository](https://github.com/velarynai/ragora-openclaw) <br>
- [Ragora MCP guide](https://ragora.app/docs?section=mcp-guide) <br>
- [Ragora getting started](https://ragora.app/docs?section=getting-started) <br>
- [Ragora API overview](https://ragora.app/docs?section=api-overview) <br>
- [Ragora retrieve API](https://ragora.app/docs?section=api-retrieve) <br>
- [Ragora errors and limits](https://ragora.app/docs?section=api-errors) <br>
- [Ragora billing API](https://ragora.app/docs?section=api-billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with source citations, tables, JSON examples, YAML/JSON configuration snippets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite returned Ragora collection and source-document metadata and avoid exposing full API keys.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
