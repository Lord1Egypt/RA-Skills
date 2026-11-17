## Description:

Save, categorize, search, and export web bookmarks with local JSON storage and tag and folder organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save URLs, organize bookmarks with tags and folders, find saved links, remove entries, and export bookmark data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML and CSV exports can produce unsafe files from saved bookmark data.

Mitigation: Treat exported HTML and CSV files as sensitive; avoid opening them in a browser or spreadsheet when bookmark fields came from untrusted sources until export escaping and CSV handling are hardened.

Risk: The skill maintains a local bookmark store and supports user-directed deletion.

Mitigation: Install only when local storage of bookmark data and deletion of saved entries fit the intended operating environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/url-bookmarker)
- [ClawHub publisher profile](https://clawhub.ai/user/fuzzyb33s)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON, HTML, or CSV bookmark exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores bookmarks in a local JSON file and can export bookmark data in JSON, HTML, or CSV format.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
