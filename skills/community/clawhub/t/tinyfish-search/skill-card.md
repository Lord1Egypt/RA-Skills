## Description:

Run web searches via TinyFish Search API and get structured JSON results (title, snippet, URL) ready for LLM consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bunsdev](https://clawhub.ai/user/bunsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve fresh web search results as structured JSON with titles, snippets, site names, URLs, and optional geo or language targeting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, plus optional location and language parameters, are sent to TinyFish.

Mitigation: Avoid confidential queries unless TinyFish account terms and data-handling expectations permit them.

Risk: The skill requires a TinyFish API key for outbound API calls.

Mitigation: Verify TINYFISH_API_KEY is present before use and handle the key as a secret.

## Reference(s):

- [TinyFish Search API documentation](https://docs.tinyfish.ai/search-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TINYFISH_API_KEY and returns ranked web search results from the TinyFish Search API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
