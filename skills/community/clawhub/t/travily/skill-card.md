## Description:

Uses Tavily AI for web search, deep research, and URL content extraction with support for search, research, and extract workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devang668](https://clawhub.ai/user/devang668)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to run Tavily-powered web searches, generate research answers with cited sources, and extract clean content from URLs through command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a bundled .env credential that appears real.

Mitigation: Remove the bundled .env credential before installation and configure a private Tavily API key locally.

Risk: Queries, URLs, and research topics are sent to Tavily.

Mitigation: Avoid submitting secrets, private internal URLs, regulated data, or confidential research topics unless that disclosure is approved.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/devang668/skills/travily)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration]

**Output Format:** [Console text or JSON, with optional saved Markdown or text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, research, and extraction outputs depend on Tavily API responses and the user's query, model, URL, and result-count options.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
