## Description:

ReadGZH lets agents retrieve public WeChat Official Account articles from supplied links as readable text or Markdown for summarization, translation, comparison, or follow-up reading through the website, remote MCP, or REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sweesama](https://clawhub.ai/user/sweesama)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to read, summarize, translate, or compare public WeChat Official Account articles from user-provided links without running a local scraper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public WeChat article URLs and request data are sent to the ReadGZH cloud service, and converted content may enter a shared cache.

Mitigation: Use only public articles that the user is authorized to submit, and avoid private, internal, sensitive, deleted, or access-restricted content.

Risk: API keys can be exposed if placed in prompts, article URLs, public files, or generated responses.

Mitigation: Keep API keys in the client's secure credential mechanism and never include them in URLs or user-visible output.

Risk: Cached search covers only articles already processed by ReadGZH and may be mistaken for full WeChat search or complete account history.

Mitigation: Treat cache search and account listings as limited cached results, and clearly report incomplete or failed article retrieval.

Risk: Repeated fresh reads can consume credits or trigger rate limits.

Mitigation: Prefer returned cached slugs for repeat access, stop repeated retries after failures, and surface insufficient-credit or rate-limit responses plainly.

## Reference(s):

- [ReadGZH ClawHub Skill Page](https://clawhub.ai/sweesama/skills/readgzh)
- [ReadGZH Website](https://readgzh.site)
- [ReadGZH Developer Docs](https://readgzh.site/docs)
- [ReadGZH OpenAPI Specification](https://readgzh.site/.well-known/openapi.yaml)
- [ReadGZH Pricing](https://readgzh.site/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text article content, optional JSON summaries, and concise configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fresh reads may consume service credits; cached reads are free, and long articles may be paginated.]

## Skill Version(s):

1.6.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
