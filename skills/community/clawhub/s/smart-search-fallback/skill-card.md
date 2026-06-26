## Description: <br>
Routes web-search requests through configured search, crawling, fetch, and vertical-search tools with automatic fallback when a provider fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep web search workflows available across English and Chinese queries by trying configured search, crawling, and fetch tools in priority order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and URLs may leave the local environment through multiple external providers. <br>
Mitigation: Do not use the skill with secrets, private repository URLs, internal hostnames, customer data, or sensitive personal information. <br>
Risk: The fallback-search helper can place raw search text into executable Python during the crawl4ai fallback. <br>
Mitigation: Review and fix the helper to URL-encode and safely pass the query before relying on it in automated workflows. <br>
Risk: Optional downstream providers require sensitive credentials. <br>
Mitigation: Store provider keys only in local environment or config files, scope them narrowly, and rotate them if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuobadaidai/smart-search-fallback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python command snippets; helper script output depends on the downstream search provider.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send queries and URLs to external search, crawling, browser, and fetch providers; optional SERPER_API_KEY and FIRECRAWL_API_KEY are used by downstream tools when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
