## Description:

Back up files uploaded to a Slack channel to the local doc/backup directory, with matching by count, filename prefix or keyword, file type, and recent upload time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caigang78](https://clawhub.ai/user/caigang78)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to back up real files from Slack into a local backup directory after describing the desired Slack file or filter in natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable behavior depends on shared Slack helper files that were outside the reviewed artifact.

Mitigation: Install or run the skill only when those shared helper files are trusted, versioned with the skill, and protected from modification.

Risk: The skill downloads real Slack files to a local backup directory.

Mitigation: Use explicit Slack backup wording, review requested filters before execution, and verify SUCCESS output plus non-empty downloaded files.

## Reference(s):

- [ClawHub Slack Backup skill page](https://clawhub.ai/caigang78/skills/slack-backup)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files, Text]

**Output Format:** [Markdown guidance with inline bash commands and SUCCESS or ERROR status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads matched Slack files to ~/.openclaw/doc/backup/ and requires success output plus a non-empty file check.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
