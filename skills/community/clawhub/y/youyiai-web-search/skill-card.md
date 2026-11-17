## Description:

SearXNG Web Search lets an agent query a configured SearXNG instance for structured web search results from Baidu, Bing, and other engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaoshaohua](https://clawhub.ai/user/qiaoshaohua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent perform public web searches, inspect structured search results, and summarize source-backed findings without browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to the default hard-coded unencrypted SearXNG endpoint.

Mitigation: Set SEARXNG_ENDPOINT or pass --endpoint with a trusted HTTPS or local self-hosted SearXNG instance, and avoid submitting secrets, private project names, personal data, or confidential text.

Risk: Search results may be incomplete, stale, unavailable, or affected by unresponsive upstream engines.

Mitigation: Use the returned source URLs to verify important claims, cite multiple reliable results for factual or news answers, and disclose when only limited results are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaoshaohua/skills/youyiai-web-search)
- [Publisher profile](https://clawhub.ai/user/qiaoshaohua)
- [Project homepage from artifact metadata](https://github.com/robydeeptool/hermes-skills)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text status output or JSON search result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 deduplicated results with title, URL, summary, and source engine; may also report empty results, errors, suggestions, or unresponsive engines.]

## Skill Version(s):

1.0.0 (source: release evidence, target metadata, frontmatter, README, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
