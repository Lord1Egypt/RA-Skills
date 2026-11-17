## Description:

Add papers from arXiv, DOI, or URL sources to Zotero via the Zotero REST API for citation management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to add research papers and web resources to a Zotero library through the Zotero REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write to Zotero account 10425097 using a named 1Password secret.

Mitigation: Install only when the agent is intended to modify that Zotero account, and prefer a release that reads the API key from the environment and makes the Zotero user ID configurable.

Risk: The skill includes deletion capability for Zotero library items.

Mitigation: Require explicit user confirmation and a current item review before running deletion operations.

Risk: The release under-discloses password-manager credential access.

Mitigation: Review credential access requirements before installation and use a Zotero API key scoped to the minimum required permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/zotero-ingest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python code examples and REST API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires outbound network access to Zotero and a Zotero API key; examples target a configured Zotero user account.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
