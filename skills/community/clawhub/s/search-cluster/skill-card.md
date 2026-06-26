## Description: <br>
Aggregated search aggregator using Google CSE, GNews RSS, Wikipedia, Reddit, and Scrapling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run aggregated web, news, encyclopedia, community, and optional scraping searches from a single interface and receive normalized results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to external search providers. <br>
Mitigation: Use the skill only for queries that are appropriate to send to the configured providers. <br>
Risk: Google Custom Search credentials may be exposed or over-scoped if configured loosely. <br>
Mitigation: Use restricted Google credentials and store them in an environment or vault appropriate for the deployment. <br>
Risk: Optional Redis caching can retain search results for 24 hours. <br>
Mitigation: Leave Redis disabled unless caching is required, and use a controlled Redis instance when enabled. <br>
Risk: The Scrapling provider runs through the Python binary set by SCRAPLING_PYTHON_PATH. <br>
Mitigation: Point SCRAPLING_PYTHON_PATH only to a trusted dedicated virtual environment with pinned dependencies. <br>


## Reference(s): <br>
- [Search APIs Reference](references/search-apis.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/1999AZZAR/search-cluster) <br>
- [Publisher Profile](https://clawhub.ai/user/1999AZZAR) <br>
- [Google Custom Search API Endpoint](https://www.googleapis.com/customsearch/v1) <br>
- [Wikipedia OpenSearch API Endpoint](https://en.wikipedia.org/w/api.php) <br>
- [Reddit Search API Endpoint](https://www.reddit.com/search.json) <br>
- [Google News RSS Search Endpoint](https://news.google.com/rss/search) <br>
- [DuckDuckGo HTML Search Endpoint](https://duckduckgo.com/html/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON search results and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include source, title, link, and sanitized snippet fields; Redis result caching is optional.] <br>

## Skill Version(s): <br>
3.5.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
