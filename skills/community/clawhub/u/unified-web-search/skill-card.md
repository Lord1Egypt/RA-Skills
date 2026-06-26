## Description: <br>
Provides a unified web search interface that routes queries across configured search providers, merges results, falls back between providers, and reports provider alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naive-white-expert](https://clawhub.ai/user/naive-white-expert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to issue web searches through one Python API while selecting search intensity, date filters, site filters, platform filters, and domestic or overseas routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, domains, date filters, platform filters, and related parameters may be sent to whichever configured third-party search provider the skill routes to or falls back to. <br>
Mitigation: Configure only providers approved for the intended data, and avoid searching for credentials, confidential internal material, private customer data, regulated content, or other sensitive information unless provider handling is permitted. <br>
Risk: Fallback routing can send a query to alternate configured providers when the preferred provider fails or returns empty results. <br>
Mitigation: Provide API keys only for providers the deployment is allowed to use, and use the documented region, platform, site, and exclude-site filters to narrow routing and results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naive-white-expert/skills/unified-web-search) <br>
- [Project homepage](https://github.com/naive-white-expert/unified-web-search) <br>
- [Provider comparison](references/comparison.md) <br>
- [Volcengine key types](references/volcengine-key-types.md) <br>
- [DashScope](https://dashscope.aliyun.com/) <br>
- [Tavily](https://tavily.com/) <br>
- [Volcengine Search API endpoint](https://open.feedcoopapi.com/search_api/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python dictionary with answer text, source metadata, provider list, alerts, and routing metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 10 deduplicated sources and may include retry hints, date range metadata, filter notes, and fallback provider details.] <br>

## Skill Version(s): <br>
2.2.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
