## Description: <br>
Provides privacy-preserving web search through a local SearXNG instance, with Docker port discovery, result aggregation, local caching, and stock-query report formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xumanzi](https://clawhub.ai/user/xumanzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to query a trusted SearXNG instance for privacy-oriented web search results. Finance-related queries are formatted as stock-analysis reports when the skill detects a stock search pattern. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discovers local Docker containers and localhost ports to find a SearXNG service. <br>
Mitigation: Set SEARXNG_URL to the exact trusted SearXNG instance for best control over where queries are sent. <br>
Risk: Search queries and results may be cached locally by the skill. <br>
Mitigation: Avoid highly sensitive queries unless you control both the SearXNG instance and the local cache location. <br>
Risk: Stock-analysis output is generated from search results and simple derived estimates. <br>
Mitigation: Treat finance reports as informational guidance and verify against authoritative market data before making decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xumanzi/web-searxng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown search results or stock-analysis reports, with plain-text status and fallback messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Caches SearXNG results locally for one hour and can return a fallback DuckDuckGo link when SearXNG is unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; changelog source: user) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
