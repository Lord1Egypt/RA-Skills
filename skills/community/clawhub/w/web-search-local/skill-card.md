## Description: <br>
Local web search without an API key, supporting Bing, DuckDuckGo, Yandex, built-in caching, and automatic failover. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnblxj](https://clawhub.ai/user/lnblxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run local web searches for recent information, reference material, and network-accessible sources without configuring a search API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to external search engines and may be cached locally for a short period. <br>
Mitigation: Avoid sensitive queries, or run with --no-cache and use --cache-clear after sensitive searches. <br>
Risk: Authenticated proxy credentials can be printed in logs when proxy URLs contain usernames or passwords. <br>
Mitigation: Avoid embedding credentials in proxy URLs unless logging is redacted or the script is changed to mask them. <br>


## Reference(s): <br>
- [Search Usage Guide](references/search-usage.md) <br>
- [Auto Engine Technical Specification](references/search-auto-engine.md) <br>
- [Engine Expansion Architecture](docs/engine-expansion.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Files] <br>
**Output Format:** [JSON or plain text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes query, engine, result count, result titles, URLs, snippets, elapsed time, and optional timing and cache metadata.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
