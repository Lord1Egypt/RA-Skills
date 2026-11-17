## Description:

Tavily Search integrates Tavily AI search with OpenClaw to provide web search, AI-powered summarization, question answering, date and domain filtering, and URL content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quenfly](https://clawhub.ai/user/quenfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Tavily for real-time web search, Q&A results, and extracted page content for RAG, market research, financial sentiment analysis, and news monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, target URLs, and extracted content requests are sent to Tavily's third-party service.

Mitigation: Avoid secrets, private or internal URLs, regulated data, and sensitive investigation topics unless third-party disclosure is approved for the environment.

Risk: The Tavily API key is required for use and may grant access to paid or quota-limited service usage.

Mitigation: Store TAVILY_API_KEY in an approved secret-management path or environment variable and rotate it according to local credential policy.

## Reference(s):

- [Tavily API Documentation Reference](references/api_docs.md)
- [Tavily](https://tavily.com/)
- [Tavily Pricing](https://tavily.com/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [JSON or Markdown search results with optional shell and Python usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; results may include titles, URLs, summaries, scores, optional answers, and extracted content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
