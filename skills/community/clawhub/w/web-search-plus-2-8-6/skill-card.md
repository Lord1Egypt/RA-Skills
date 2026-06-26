## Description: <br>
Unified search skill with Intelligent Auto-Routing that selects among Serper, Tavily, Exa, Perplexity, You.com, and SearXNG using multi-signal query analysis and confidence scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marsxuc](https://clawhub.ai/user/marsxuc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run current web searches through a single interface that can choose an appropriate provider, return source-linked results, and explain or override routing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, and optional full-content retrieval may be sent to the configured external provider and cached locally. <br>
Mitigation: Configure only providers you intend to use, use SearXNG for privacy-sensitive searches, and use no-cache or cache-clearing options when local retention is not desired. <br>
Risk: Provider selection can route ambiguous queries to a less suitable search provider. <br>
Mitigation: Use routing explanations and explicit provider overrides when search intent or privacy requirements are important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marsxuc/web-search-plus-2-8-6) <br>
- [Serper](https://serper.dev) <br>
- [Tavily](https://tavily.com) <br>
- [Exa](https://exa.ai) <br>
- [Kilo Gateway](https://kilo.ai) <br>
- [You.com API](https://api.you.com) <br>
- [SearXNG documentation](https://docs.searxng.org) <br>
- [Perplexity](https://www.perplexity.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output can include provider, query, result titles, URLs, snippets, scores, cache metadata, and routing confidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill artifact version 2.8.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
