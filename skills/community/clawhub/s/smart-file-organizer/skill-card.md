## Description:

Organizes local files into AI-generated Johnny Decimal categories, asks the user to confirm the proposed plan, and can check for duplicate files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akira82-ai](https://clawhub.ai/user/akira82-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize an explicitly chosen source folder into semantic Johnny Decimal categories in a target folder. The skill presents a classification plan for review before moving files and can produce duplicate-file reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move or permanently delete local files.

Mitigation: Use it only on a small, explicitly chosen folder, keep backups, and review the move plan carefully before approving changes.

Risk: The duplicate-delete option relies on MD5 duplicate detection and permanent deletion.

Mitigation: Avoid automatic duplicate deletion unless safer hashing, byte comparison, and trash or quarantine behavior are implemented.

## Reference(s):

- [Johnny Decimal Reference](references/johnny_decimal.md)
- [ClawHub Skill Page](https://clawhub.ai/akira82-ai/skills/smart-file-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with inline shell commands and file organization summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source and target folder prompts, classification plans, confirmation requests, duplicate reports, and final organization summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
