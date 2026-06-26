## Description: <br>
Web search via the Tavily API for agents that need to look up sources, find links, return concise result sets, and optionally include short answer summaries when Brave web search is unavailable or undesired. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[confidentkai](https://clawhub.ai/user/confidentkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Tavily web searches, retrieve titles, URLs, snippets, and optional answer summaries, and choose JSON, Brave-compatible JSON, Markdown, or text output for downstream agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily and recent query/results may be stored in a local cache. <br>
Mitigation: Avoid sensitive searches, use --no-cache for sensitive queries, and keep the cache directory at the default application-owned path. <br>
Risk: Verbose mode and API-key inspection examples can expose the Tavily API key in command output. <br>
Mitigation: Avoid --verbose and key-inspection examples unless outputs are redacted and shared only in trusted environments. <br>
Risk: Clearing cache with a broad custom cache path can remove more local data than intended. <br>
Mitigation: Use the default cache path and avoid --clear-cache when TAVILY_CACHE_DIR points to a broad or shared directory. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [ClawHub release page](https://clawhub.ai/confidentkai/tavily-search-optimized-v1) <br>
- [Publisher profile](https://clawhub.ai/user/confidentkai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON, Brave-compatible JSON, Markdown, or plain text returned by a command-line search tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tavily API key; supports max results, answer summaries, search depth, timeout, cache TTL, cache disabling, cache clearing, and verbose mode.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter and changelog list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
