## Description:

Search X (Twitter) posts using the xAI API. Use when the user wants to find tweets, search X/Twitter, look up what people are saying on X, or find social media posts about a topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github2cao](https://clawhub.ai/user/github2cao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search and summarize X/Twitter posts through xAI's X search tooling, with optional handle filters, exclusion filters, date ranges, and image or video understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search text, handle filters, date filters, and media options are sent to xAI/X services under the user's XAI_API_KEY.

Mitigation: Avoid secrets, private business information, and personal data in search queries or filters.

Risk: Use of the configured XAI_API_KEY may incur provider usage costs.

Mitigation: Run the skill only with an intended xAI account and monitor provider-side usage and billing.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/github2cao/skills/ssdfsdfsdfsaaaaaaa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-formatted command output from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include post text, authors, status, citations, search-call counts, and token usage returned by the xAI API.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
