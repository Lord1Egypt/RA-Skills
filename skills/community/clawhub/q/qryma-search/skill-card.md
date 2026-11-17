## Description:

Qryma AI Search retrieves Web information and returns LLM-friendly data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qryma888](https://clawhub.ai/user/qryma888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve web search results from the Qryma API and return them as Markdown or JSON for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Qryma API key and can read credentials from environment variables or local .env files.

Mitigation: Use QRYMA_API_KEY from a protected environment variable or carefully permissioned config file, avoid pasting real keys into chat, and avoid running from untrusted directories that may contain .env files.

Risk: The skill supports a configurable QRYMA_ENDPOINT, which could send queries and API keys to an untrusted destination if misconfigured.

Mitigation: Keep the default endpoint unless the replacement endpoint is fully trusted and reviewed.

Risk: The server security verdict is suspicious because this is a real web-search skill that handles API keys.

Mitigation: Review the skill before installation and scan it before deployment, following the server-provided security guidance.

## Reference(s):

- [Qryma Search on ClawHub](https://clawhub.ai/qryma888/skills/qryma-search)
- [Qryma](https://qryma.com)
- [Google Interface Language Codes](https://developers.google.com/custom-search/docs/xml_results_appendices#interfaceLanguages)
- [Qryma Search API Endpoint](https://search.qryma.com/api/web)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON search results, with shell commands and configuration guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports raw JSON, Brave-compatible JSON, and human-readable Markdown output; result count is capped at 10 by the CLI.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
