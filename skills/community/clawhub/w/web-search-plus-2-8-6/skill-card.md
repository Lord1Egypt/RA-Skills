## Description:

Unified search skill with Intelligent Auto-Routing. Uses multi-signal analysis to automatically select between Serper (Google), Tavily (Research), Exa (Neural), Perplexity (AI Answers), You.com (RAG/Real-time), and SearXNG (Privacy/Self-hosted) with confidence scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marsxuc](https://clawhub.ai/user/marsxuc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route web searches across configured providers for product lookup, research, similar-page discovery, direct answers, real-time search, and privacy-oriented SearXNG searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to whichever external provider is configured or selected by routing.

Mitigation: Use only providers approved for the data being searched and avoid submitting sensitive or confidential queries.

Risk: API keys and cached search history may be stored locally by the skill.

Mitigation: Prefer environment variables or a permissioned secrets store for keys, keep local config files private, and disable or clear caching for sensitive searches.

Risk: A configured SearXNG instance URL may reach internal network services if URL protection is bypassed.

Mitigation: Use a trusted pinned SearXNG deployment and review SearXNG instance configuration before enabling it.

Risk: The included test script may load values from an untrusted .env file.

Mitigation: Run tests only from trusted workspaces and inspect local environment files before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marsxuc/skills/web-search-plus-2-8-6)
- [Publisher Profile](https://clawhub.ai/user/marsxuc)
- [Serper](https://serper.dev)
- [Tavily](https://tavily.com)
- [Exa](https://exa.ai)
- [Perplexity](https://www.perplexity.ai)
- [You.com API](https://api.you.com)
- [SearXNG Documentation](https://docs.searxng.org)
- [SearXNG Installation](https://docs.searxng.org/admin/installation.html)
- [Kilo](https://kilo.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results plus Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results can include provider, query, result items, scores, routing confidence, fallback status, and cache metadata.]

## Skill Version(s):

2.8.6 (source: SKILL.md frontmatter, package.json, CHANGELOG; ClawHub release 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
