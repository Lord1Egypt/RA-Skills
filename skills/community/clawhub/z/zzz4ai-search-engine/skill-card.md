## Description:

A China-focused search aggregation skill that selects among six available search sources for general web, academic, news, and video queries, with advanced search syntax and intent-based routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingshangfei](https://clawhub.ai/user/bingshangfei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Chinese-language web, academic, news, and video sources without an API key. It is intended for information lookup, comparison, recommendations, rankings, recent updates, academic-paper discovery, and Bilibili or Toutiao content discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms can cause ordinary questions to be routed to third-party search providers without clear user intent.

Mitigation: Review the query and selected provider before searching, especially for private, proprietary, legal, employment, credential, or otherwise sensitive topics.

Risk: Search terms are sent to external providers including Bing CN, 360, Toutiao, and Bilibili.

Mitigation: Use the skill only when third-party search disclosure is acceptable and avoid sensitive topics unless the user explicitly approves the search plan.

## Reference(s):

- [Advanced Search Guide](references/advanced-search.md)
- [ClawHub Skill Page](https://clawhub.ai/bingshangfei/skills/zzz4ai-search-engine)
- [Publisher Profile](https://clawhub.ai/user/bingshangfei)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown search report with result titles, summaries, source names, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider failure notes, fallback-engine behavior, and suggestions to refine the query when all engines fail.]

## Skill Version(s):

1.0.6 (source: release evidence and CHANGELOG, released 2026-05-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
