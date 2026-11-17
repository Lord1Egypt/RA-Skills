## Description:

Push X/Twitter bookmarks into Google NotebookLM notebooks, auto-routed by bookmark folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch their X/Twitter bookmarks, route them by bookmark folder, and add bookmark-derived text sources to matching Google NotebookLM notebooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses exported X session cookies and sends bookmark-derived text, author handles, and source URLs to Google NotebookLM.

Mitigation: Install only after review, store cookie files with restrictive permissions, and confirm the destination notebook before uploading bookmark content.

Risk: The security scan reports unsafe command construction and under-disclosed persistent data transfer.

Mitigation: Avoid unattended sync until command construction is fixed and the workflow requires explicit confirmation before uploads.

Risk: The security guidance calls out unpinned dependencies.

Mitigation: Pin and review dependencies before using the skill in a persistent or commercial environment.

## Reference(s):

- [X To Notebook ClawHub Skill Page](https://clawhub.ai/spideystreet/skills/x-to-notebook)
- [twikit](https://github.com/d60/twikit)
- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with inline shell commands and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces progress summaries and error messages while syncing bookmarks; helper scripts emit JSON for folders, bookmarks, and unattended sync reports.]

## Skill Version(s):

1.1.0 (source: server release metadata and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
