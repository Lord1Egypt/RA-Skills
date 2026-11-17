## Description:

Extract clean article content from URLs through the AISA Tavily extract endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to extract readable page content from known URLs for summarization, comparison, or evidence review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runtime exposes broader search, research, and synthesis commands beyond URL extraction.

Mitigation: Review the bundled client before installing and restrict or remove commands that are not needed for URL extraction.

Risk: User URLs, search queries, prompts, and aggregated results may be sent to external AISA endpoints under the configured API key.

Mitigation: Use the skill only for data approved for external API processing and configure AISA_API_KEY according to the deployment's credential handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/tavily-extract-aisa)
- [AISA service](https://aisa.one)
- [AISA API base](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and extracted API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; runtime sends requests to external AISA endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
