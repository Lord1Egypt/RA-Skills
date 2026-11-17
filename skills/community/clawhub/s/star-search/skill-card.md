## Description:

Star Search helps agents search the web, retrieve Chinese and English online information, perform finance and technology news lookups, and return LLM-assisted answers through MCP, JSON-RPC, SSE, CLI, LangChain, and Dify integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muchenhengxin](https://clawhub.ai/user/muchenhengxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Star Search as a multi-engine web search and answer layer for research, current information lookup, Chinese web coverage, finance and technology news, and MCP-based tool access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports under-secured public API, account, payment, URL-fetching, and credential-handling behavior.

Mitigation: Use only in an isolated development environment until deployment hardening is complete.

Risk: URL fetching and external LLM/search calls can create unintended network exposure.

Mitigation: Block private and internal URL fetches, require HTTPS allowlisted egress, and use a dedicated LLM key.

Risk: Public or costly endpoints may be abused if exposed without controls.

Mitigation: Require authentication, quotas, and reviewed payment callback handling before public deployment.

Risk: Credential and authorization defaults require review before production use.

Mitigation: Remove the Hermes auth-file fallback, replace hard-coded token secrets and password hashing, and avoid automatically granting Cloudflare WAF or bot-management permissions to an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muchenhengxin/skills/star-search)
- [Camofox API Quick Reference](artifact/references/camofox-api.md)
- [Search Engine Research](artifact/references/search-engine-research.md)
- [v15.1 site:bing probe results](artifact/references/v15-site-bing-probe-results.md)
- [v16 engine addition checklist](artifact/references/v16-engine-addition-checklist.md)
- [v16.1 RSS probe results](artifact/references/v16-rss-probe-results.md)
- [Star Search vs Baidu Search comparison](artifact/references/vs-baidu-search-comparison.md)
- [v20.102 end-to-end pipeline fix](artifact/references/实战102-end-to-end-pipeline-fix.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with optional JSON, table, and Mermaid output modes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can provide search results, citations, source summaries, streamed answer chunks, MCP tool responses, integration snippets, and setup commands.]

## Skill Version(s):

20.42.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
