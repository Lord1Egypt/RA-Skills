## Description:

WizNote connects an agent to WizNote so it can list, search, read, create, update, delete, share, comment on, and manage notes, categories, tags, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfengxiang](https://clawhub.ai/user/wangfengxiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to operate a WizNote workspace through natural-language or MCP-style workflows, including note retrieval, Markdown-based note creation, attachment handling, sharing, and note organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports apparent real credentials and private endpoint or account examples in the skill material.

Mitigation: Treat those credentials as compromised, rotate them, and remove private endpoint and account examples before installation or publication.

Risk: The skill can delete, share, upload, download, and import content from URLs, which can affect user data and expose note contents.

Mitigation: Require explicit user confirmation for destructive or sharing operations, URL imports, uploads, and downloads.

Risk: The security evidence warns about unsafe handling of note data, network requests, and local files.

Mitigation: Use HTTPS/WSS, restrict URL fetching, sanitize download paths, and run the skill with pinned dependencies in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangfengxiang/skills/wiznote)
- [Publisher profile](https://clawhub.ai/user/wangfengxiang)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration]

**Output Format:** [Markdown, text, and JSON-like API responses with occasional shell or Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may create, modify, share, upload, download, or delete WizNote content when connected to a configured WizNote account.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
