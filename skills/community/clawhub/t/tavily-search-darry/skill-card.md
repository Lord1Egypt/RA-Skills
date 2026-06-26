## Description: <br>
Tavily Search integrates Tavily APIs for web search, news lookup, content extraction, site crawling, and multi-source research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarryEK](https://clawhub.ai/user/DarryEK) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill to run Tavily-backed search, extraction, crawling, and research workflows from an agent without writing a custom API integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, and extracted web content are sent to Tavily during normal use. <br>
Mitigation: Avoid submitting secrets, internal-only URLs, or sensitive research prompts unless Tavily processing is approved for that data. <br>
Risk: The skill can read Tavily OAuth tokens from ~/.mcp-auth when TAVILY_API_KEY is not set. <br>
Mitigation: Prefer setting TAVILY_API_KEY explicitly in the agent environment and review local OAuth token access before use. <br>
Risk: First-run authentication can launch an npm-based OAuth helper. <br>
Mitigation: Review and approve the helper execution path before first use, especially in managed or production environments. <br>
Risk: Crawling can create broad external requests and write markdown files to user-provided output paths. <br>
Mitigation: Use conservative crawl depth, breadth, and limit settings, and choose bounded output directories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DarryEK/tavily-search-darry) <br>
- [Tavily](https://tavily.com) <br>
- [Search API Reference](artifact/tavily-best-practices/references/search.md) <br>
- [Extract API Reference](artifact/tavily-best-practices/references/extract.md) <br>
- [Crawl & Map API Reference](artifact/tavily-best-practices/references/crawl.md) <br>
- [Research API Reference](artifact/tavily-best-practices/references/research.md) <br>
- [SDK Reference](artifact/tavily-best-practices/references/sdk.md) <br>
- [Framework Integrations](artifact/tavily-best-practices/references/integrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-oriented shell/API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save crawl and research outputs to local markdown files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
