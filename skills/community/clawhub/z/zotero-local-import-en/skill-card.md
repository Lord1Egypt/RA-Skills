## Description:

Import local PDF files into Zotero from the command line on Windows, macOS, or Linux through the Zotero local connector at 127.0.0.1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to import one PDF, selected PDFs, or folders of PDFs into an existing Zotero library or collection through a locally running Zotero Desktop instance. It can also list existing local collections and check recent Zotero attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The doctor command can install an unpinned requests dependency and modify the Python environment.

Mitigation: Install dependencies manually in a dedicated virtual environment with a pinned requests version before running the skill, and avoid --auto-install-deps unless the user explicitly approves it.

Risk: The import workflow reads user-selected PDFs or folders and sends the PDF contents to the local Zotero connector.

Mitigation: Use only explicit user-provided paths, confirm the Zotero connector port, and avoid importing files whose contents the user has not approved for local processing.

Risk: The check command can read attachment metadata from the user's local Zotero database.

Mitigation: Run check only when the user asks to verify recent imports, and use the default read-only behavior or an explicitly supplied database path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mxingchtongaelofficial2568/skills/zotero-local-import-en)
- [Publisher profile](https://clawhub.ai/user/mxingchtongaelofficial2568)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided local PDF paths, Zotero connector port, optional collection name, and local Zotero Desktop access.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
