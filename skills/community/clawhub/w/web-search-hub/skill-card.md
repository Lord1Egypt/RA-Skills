## Description:

Searches web pages, news, images, and videos through DuckDuckGo with filters for recency, region, safe search, media properties, result count, and text, Markdown, or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anisafifi](https://clawhub.ai/user/anisafifi)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, researchers, and external users use this skill to gather current web, news, image, and video search results for research, fact-checking, market monitoring, and visual resource discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an apparently unused external CLI and an unpinned Python dependency before use.

Mitigation: Review the prerequisite need before deployment, install dependencies in a virtual environment, and pin and verify duckduckgo-search where possible.

Risk: Search queries may expose secrets, private project names, or sensitive personal data to an external search provider.

Mitigation: Do not send secrets, confidential identifiers, or sensitive personal data as search queries.

## Reference(s):

- [Web Search Hub on ClawHub](https://clawhub.ai/anisafifi/skills/web-search-hub)
- [OpenClawCLI](https://clawhub.ai/)
- [duckduckgo-search Python package](https://pypi.org/project/duckduckgo-search/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text, Markdown, or JSON search results, with optional saved files and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports web, news, image, and video result structures with optional region, time range, safe search, result count, image, and video filters.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
