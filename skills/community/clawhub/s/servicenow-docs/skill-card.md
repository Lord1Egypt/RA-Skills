## Description:

Search and retrieve ServiceNow documentation, release notes, and developer docs (APIs, references, guides). Uses docs.servicenow.com via Zoomin and developer.servicenow.com APIs for developer topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Developers, administrators, and support teams use this skill to find and summarize ServiceNow product documentation, release notes, API references, and developer guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The article-fetch tool can request arbitrary URLs from the agent runtime instead of being limited to ServiceNow documentation hosts.

Mitigation: Run the skill only where outbound network access is restricted, or update the article-fetch tool to allow only HTTPS ServiceNow documentation hosts and validate redirects.

Risk: The dependency range may reduce install reproducibility.

Mitigation: Pin the dependency version before release or installation.

## Reference(s):

- [ServiceNow product documentation](https://docs.servicenow.com/)
- [ServiceNow developer documentation](https://developer.servicenow.com/)
- [ClawHub skill page](https://clawhub.ai/thesethrose/skills/servicenow-docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with documentation links, search results, and concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some fetched article and guide outputs are truncated; developer API reference search returns URLs for browser access.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
