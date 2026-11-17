## Description:

Local web search without API Key. Supports Bing, DuckDuckGo, Yandex multi-engine search with built-in cache and automatic failover. Use when users need to search for network information, find materials, or query real-time information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnblxj](https://clawhub.ai/user/lnblxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run local web searches for current information and reference material without configuring a search API key. It is suited to CLI-driven search workflows that need JSON or text results from Bing, DuckDuckGo, Yandex, or fallback fetching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to external search engines and may reveal sensitive or private information.

Mitigation: Avoid sensitive, private, or secret-containing queries unless the user explicitly accepts that disclosure.

Risk: Search results are cached locally for about one hour by default.

Mitigation: Use --no-cache for sensitive searches and --cache-clear to remove stored result files.

Risk: Proxy credentials embedded in proxy URLs can appear in logs.

Mitigation: Use proxy configuration without embedded credentials, restrict log access, or avoid verbose logging when credentials are present.

## Reference(s):

- [Web Search Local Skill Page](https://clawhub.ai/lnblxj/skills/web-search-local)
- [README](README.md)
- [Search Usage Guide](references/search-usage.md)
- [Auto Engine Technical Specification](references/search-auto-engine.md)
- [Engine Expansion Design](docs/engine-expansion.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, files, guidance]

**Output Format:** [JSON or plain text search results, with optional output files and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result objects include query, engine, result count, titles, URLs, snippets, elapsed time, and timing metadata; cached results may include a cache_hit marker.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
