## Description:

Interact with Confluence Cloud via REST API for space management, page operations, CQL search, page tree navigation, attachments, comments, and labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation owners, and operations teams use this skill to manage Confluence Cloud spaces, pages, attachments, comments, labels, searches, and page trees from an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise broad live Confluence workspace authority through an Atlassian API token.

Mitigation: Use a narrowly scoped API token and verify CONFLUENCE_BASE_URL is exactly the intended HTTPS Confluence tenant before running commands.

Risk: Delete and purge operations can remove pages or attachments, including permanent deletion when purge flags are used.

Mitigation: Require explicit human confirmation for delete-page, delete-attachment, delete-comment, remove-label, and any purge command before execution.

Risk: Attachment downloads can write files to local paths chosen by command arguments or attachment titles.

Mitigation: Use an explicit safe output path for downloads and inspect downloaded files before opening or reusing them.

Risk: Raw curl workflows can bypass the script's narrower command interface.

Mitigation: Prefer the provided confluence.py operations and use raw curl only when the requested API action is not otherwise available.

## Reference(s):

- [Confluence Storage Format Reference](references/storage-format.md)
- [Confluence Query Language (CQL) Reference](references/cql.md)
- [Atlassian Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)
- [Atlassian Confluence Cloud REST API v1](https://developer.atlassian.com/cloud/confluence/rest/v1/intro/)
- [Snowsand Confluence on ClawHub](https://clawhub.ai/snowsand-enterprises/skills/snowsand-confluence)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration notes, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Confluence Cloud URL, user email, and API token environment variables before live API operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
