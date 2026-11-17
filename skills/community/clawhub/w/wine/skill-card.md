## Description:

Record, search, and analyze wine collection entries, tasting notes, vintages, ratings, and inventory from a local command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Wine to log, search, summarize, and export wine-related notes and inventory records through local terminal commands. Users should review the publisher-noted mismatch between the wine management description and the shipped generic local logging behavior before installing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as wine management but ships a generic local logging script.

Mitigation: Review the commands and local storage behavior before installation to confirm the skill matches the intended use.

Risk: Command inputs may be stored in local logs and exported files.

Mitigation: Avoid entering sensitive personal, business, credential, or account information unless the publisher clarifies data handling, retention, export behavior, and deletion controls.

## Reference(s):

- [Wine on ClawHub](https://clawhub.ai/ckchzh/skills/wine)
- [Publisher Profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Terminal text output and exported JSON, CSV, or plain-text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command inputs and history in local files under ~/.local/share/wine/.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
