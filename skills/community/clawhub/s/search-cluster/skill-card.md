## Description:

Aggregates search results from Google Custom Search, Google News RSS, Wikipedia, Reddit, and Scrapling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Developers and agents use Search Cluster to issue a query across multiple external search providers and receive normalized search results with source, title, link, and snippet fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to external providers, including DuckDuckGo through Scrapling.

Mitigation: Install only when external search-provider disclosure is acceptable for the intended queries.

Risk: The Scrapling provider runs through a configured Python subprocess and dependency environment.

Mitigation: Use a trusted SCRAPLING_PYTHON_PATH virtual environment and pin or review Scrapling dependencies before use.

Risk: Redis caching can retain search results for 24 hours when REDIS_HOST is configured.

Mitigation: Enable Redis only when temporary caching of query-derived results is acceptable.

Risk: Secrets or sensitive data could be exposed if placed in custom user-agent values or search queries.

Mitigation: Keep secrets out of SEARCH_USER_AGENT and query text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1999azzar/skills/search-cluster)
- [Search APIs Reference](artifact/references/search-apis.md)
- [Google Custom Search API](https://www.googleapis.com/customsearch/v1)
- [Wikipedia OpenSearch API](https://en.wikipedia.org/w/api.php)
- [Reddit Search API](https://www.reddit.com/search.json)
- [Google News RSS Search](https://news.google.com/rss/search)
- [DuckDuckGo HTML Search](https://duckduckgo.com/html/)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [JSON array of search result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each result may include source, title, link, and sanitized snippet fields.]

## Skill Version(s):

3.5.1 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
