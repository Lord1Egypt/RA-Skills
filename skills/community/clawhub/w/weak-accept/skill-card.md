## Description:

Fetch arXiv paper lists, display paper details and public comments, and submit short reviews through the configured arXiv Crawler API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxrys](https://clawhub.ai/user/zxrys)

### License/Terms of Use:


## Use Case:

Developers and research workflow users use this skill to query arXiv paper metadata, inspect comments, and add short public reviews from an agent-assisted command-line flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, author names, and comments may be exposed because the configured endpoint uses unencrypted HTTP.

Mitigation: Do not configure an API key or submit private comments unless the endpoint is changed to HTTPS and the server is trusted.

Risk: Submitted comments are sent to a public remote service and may become public remote data.

Mitigation: Treat submitted comments as public and avoid including confidential or personal information.

Risk: The installer installs the requests dependency without a pinned version.

Mitigation: Prefer pinned dependencies and review the install step before deployment.

Risk: Running the installer with elevated privileges could broaden the impact of dependency or environment changes.

Mitigation: Avoid running the installer as root; use an isolated virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxrys/skills/weak-accept)
- [Configured arXiv Crawler API endpoint](http://150.158.152.82:8000)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and text or JSON-like API results from the Python client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The client prints paper lists, paper details, comment lists, success messages, and HTTP error text to stdout.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
