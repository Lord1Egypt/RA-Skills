## Description:

webserp runs parallel web searches across seven engines with browser impersonation and returns SearXNG-compatible JSON results for current-information lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperboardofficial](https://clawhub.ai/user/paperboardofficial)

### License/Terms of Use:


## Use Case:

Developers and agents use webserp to find current web information, verify facts, discover URLs, and collect source snippets when answers require information beyond training data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to external search providers and may expose secrets, personal data, or confidential business text.

Mitigation: Do not include secrets, credentials, personal data, or confidential business information in search queries.

Risk: The install command uses an unpinned third-party pip package.

Mitigation: Install in a virtual environment or other low-privilege context and review or pin the webserp package before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paperboardofficial/skills/webserp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed CLI emits SearXNG-compatible JSON containing query metadata, result entries, suggestions, and unresponsive engine details.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
