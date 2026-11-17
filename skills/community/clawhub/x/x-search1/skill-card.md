## Description:

Search X (Twitter) posts using the xAI API when users want to find tweets, look up what people are saying on X, or find social media posts about a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github2cao](https://clawhub.ai/user/github2cao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run real-time X/Twitter searches through xAI, with optional handle filters, date ranges, media understanding, and citations to original posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, handles, date filters, and media options are sent to xAI.

Mitigation: Avoid using secrets, confidential business data, private incident details, or sensitive personal information in searches.

Risk: Search results and summaries may be incomplete, time-sensitive, or misleading.

Mitigation: Review cited original X posts before acting on results or presenting them as authoritative.

Risk: The skill depends on an xAI API key and external network access.

Mitigation: Use an API key with only the access needed for xAI search and rotate or revoke it if exposed.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI console](https://console.x.ai)
- [xAI Responses API endpoint](https://api.x.ai/v1/responses)
- [ClawHub skill page](https://clawhub.ai/github2cao/skills/x-search1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON results containing status, query text, response text, citations, search count, and token usage; agent-facing guidance may be presented as Markdown with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and XAI_API_KEY; supports allowed or excluded handles, date ranges, image understanding, and video understanding.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
