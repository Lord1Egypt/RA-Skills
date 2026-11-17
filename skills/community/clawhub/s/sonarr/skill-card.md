## Description:

Search and add TV shows to Sonarr with monitor options and search-on-add support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordyvandomselaar](https://clawhub.ai/user/jordyvandomselaar)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Sonarr for TV shows, add selected series to a Sonarr library, check existing library entries, and remove shows when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remove shows from Sonarr and can use --delete-files, which may delete media managed by Sonarr.

Mitigation: Confirm removal and file deletion explicitly before running the command; avoid --delete-files unless the user has approved deletion.

Risk: The skill requires a Sonarr API key in local configuration, and logs may expose operational details.

Mitigation: Keep the Sonarr config file private and rotate the API key if process logs may have captured command arguments or credentials.

## Reference(s):

- [ClawHub Sonarr skill page](https://clawhub.ai/jordyvandomselaar/skills/sonarr)
- [jordyvandomselaar publisher profile](https://clawhub.ai/user/jordyvandomselaar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands, plain-text command output, and JSON output for search-json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq plus a Sonarr URL and API key in local configuration.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
