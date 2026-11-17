## Description:

Use this skill when a user asks for SEO keyword research, keyword discovery, search volume analysis, keyword difficulty, search intent mapping, topic clusters, content opportunities, competitor keyword gaps, or a keyword strategy for a domain, URL, product, market, or seed topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO practitioners use this skill to crawl public websites, query AIsa/DataForSEO keyword and SERP data, cluster opportunities by intent, and produce actionable keyword strategy reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website URLs, competitor names, and SEO strategy inputs may be sent to AIsa/DataForSEO during keyword and SERP research.

Mitigation: Use the skill only with public SEO research data that is acceptable to share with those services.

Risk: Bundled network helpers use AISA_API_KEY and make outbound requests.

Mitigation: Review or restrict the helpers so the API key is sent only to api.aisa.one and is never printed, committed, or reused for unrelated endpoints.

Risk: The crawler can fetch user-provided URLs and follow same-site links.

Mitigation: Avoid private or internal URLs and restrict crawler access to prevent internal network requests or unsafe redirects before deployment.

## Reference(s):

- [AIsa API Map for SEO Keyword Research](references/aisa-api-map.md)
- [Keyword Research Report Template](references/report-template.md)
- [AIsa](https://aisa.one)
- [AIsa Data APIs](https://api.aisa.one/apis/v1)
- [AIsa LLM Gateway](https://api.aisa.one/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and optional JSON data exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include research assumptions, crawled-site profile, keyword clusters, metrics tables, SERP-based page recommendations, validation notes, and API-derived JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
