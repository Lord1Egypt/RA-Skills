## Description:

Search and add TV shows to Sonarr, with monitor options and search-on-add support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frannunpal](https://clawhub.ai/user/frannunpal)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage a Sonarr library by searching TV shows, checking whether a TVDB ID exists, and adding or removing shows through Sonarr API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remove shows from Sonarr and can delete media files when remove is run with --delete-files.

Mitigation: Confirm the exact TVDB ID and deletion choice with the user before running remove, and avoid --delete-files unless the user explicitly accepts file deletion.

Risk: The skill requires a Sonarr API key with library mutation rights.

Mitigation: Use only a Sonarr API key the user is comfortable granting for library changes, and keep it in the documented config file or environment variables.

## Reference(s):

- [Sonarr Fixed skill page](https://clawhub.ai/frannunpal/skills/sonarr-fixed)
- [Original Sonarr skill](https://clawhub.com/jordyvandomselaar/sonarr)
- [Original publisher profile](https://clawhub.com/jordyvandomselaar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash command examples; runtime command output is plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, a Sonarr URL, a Sonarr API key, and optional default quality profile configuration.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
