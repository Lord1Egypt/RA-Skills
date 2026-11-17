## Description:

Use when you need fresh web results through Volcengine ARK Responses API, especially for today's news, recent updates, fact checks, topic monitoring, or Chinese-language search workflows powered by ARK_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henry-insomniac](https://clawhub.ai/user/henry-insomniac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route current public web research through Volcengine ARK, then return concise summaries with explicit dates and source links. It is especially suited to recent-news, fact-checking, topic-monitoring, and Chinese-language search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key-bearing requests could be redirected if ARK_BASE_URL or --base-url is set to an untrusted endpoint.

Mitigation: Use only a trusted HTTPS Volcengine endpoint and avoid overriding ARK_BASE_URL or --base-url unless the endpoint has been approved.

Risk: Search queries and prompts are sent to Volcengine ARK and may include sensitive or regulated information.

Mitigation: Use the skill only where ARK_API_KEY is intended for this service, and avoid sensitive or regulated queries unless policy allows sending them to Volcengine.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/henry-insomniac/skills/volcengine-ark-web-search)
- [Volcengine Responses API Documentation](https://www.volcengine.com/docs/82379/1783703?lang=zh)
- [ARK Responses API Notes](references/ark-responses-api.md)
- [Volcengine Responses Streaming Article](https://developer.volcengine.com/articles/7563963410168569894)
- [Volcengine Web Search Article](https://developer.volcengine.com/articles/7565184101091639338)
- [Volcengine Web Search API Reference](https://www.volcengine.com/docs/82379/1958524?lang=zh)
- [Volcengine Common Online Inference Documentation](https://www.volcengine.com/docs/82379/2121998?lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown summaries with title, summary, and sources sections by default; optional JSON or raw API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese-oriented summaries, explicit dates for relative-time queries, source-link extraction, streaming support, dry-run output, and retry handling for transient API failures.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
