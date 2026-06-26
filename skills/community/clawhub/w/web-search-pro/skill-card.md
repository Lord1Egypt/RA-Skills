## Description: <br>
Agent-first web search and retrieval for live web search, news search, docs lookup, code lookup, company research, site crawl, site map, and structured evidence packs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zjianru](https://clawhub.ai/user/Zjianru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add live web search, news search, documentation lookup, extraction, crawling, site mapping, and research-pack assembly to an agent workflow. It supports a no-key baseline and optional provider credentials for broader retrieval coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, submitted URLs, and retrieved content may be sent to configured third-party search or retrieval providers. <br>
Mitigation: Configure only provider API keys and endpoints that are acceptable for the intended data, and avoid private URLs or secret-bearing query strings. <br>
Risk: Live web retrieval can return incomplete, stale, or misleading content from external sources. <br>
Mitigation: Use the skill's routing diagnostics, citations, and federated-search signals to review important outputs before relying on them. <br>
Risk: Network-capable crawling and extraction can expand the amount of untrusted web content processed by the agent. <br>
Mitigation: Keep the documented safe-fetch boundary enabled, including HTTP(S)-only access, redirect revalidation, blocked localhost/private/metadata targets, and disabled JavaScript execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zjianru/web-search-pro) <br>
- [ClawHub compliance notes](docs/clawhub-compliance.md) <br>
- [Project homepage](https://github.com/Zjianru/web-search-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON or Markdown from local Node CLI commands, including search results, extracted page text, crawl or map summaries, routing diagnostics, and research packs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node. The baseline runs without API keys; optional provider credentials and endpoints widen retrieval coverage and may send queries, URLs, and retrieved content to configured providers.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release metadata, released 2026-03-14T07:38:43Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
