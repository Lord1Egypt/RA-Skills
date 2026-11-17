## Description:

Calls a Volcengine web search integration to retrieve web, summarized web, or image search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run web, summarized web, or image searches and inspect returned summaries, counts, usage, and result links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and the AZT API key are sent to a third-party proxy service.

Mitigation: Use a dedicated, low-privilege, revocable key and avoid secret, personal, regulated, or internal queries.

Risk: Passing the API key as a command-line argument can expose it through shell history or process inspection.

Mitigation: Prefer the AZT_API_KEY environment variable for key handling.

Risk: The security review notes broad activation language and limited consent or data-handling disclosure.

Mitigation: Confirm user intent before external searches and disclose that requests are handled through a third-party proxy integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyriswu/skills/volcengine-web-search-online)
- [Devtool plugin documentation](https://devtool.uk/plugin)
- [Volcengine web search endpoint](https://coze-js-api.devtool.uk/volcengine/web-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown search results with optional raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires query, search_type, and an AZT_API_KEY value; supports optional count, summary, time range, content format, industry, and query rewrite settings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
