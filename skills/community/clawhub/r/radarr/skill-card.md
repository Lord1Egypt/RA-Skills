## Description:

Searches for and adds movies to Radarr with collection support and optional search-on-add behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordyvandomselaar](https://clawhub.ai/user/jordyvandomselaar)

### License/Terms of Use:


## Use Case:

Media server operators with a Radarr instance use this skill to search for movies, add individual movies or collections, inspect Radarr configuration options, and remove library entries through Radarr API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remove Radarr library entries and can delete media files when remove is used with --delete-files.

Mitigation: Require explicit user confirmation before removing movies, and only use --delete-files after confirming that the user intends to delete media files.

Risk: Adding a collection can enable persistent collection monitoring and future automatic additions.

Mitigation: Explain the monitoring and search-on-add behavior before add-collection, and confirm the user's intent before enabling ongoing collection monitoring.

Risk: The Radarr API key is used for library mutation and is stored in a local credential file.

Mitigation: Use an API key appropriate for library mutation, protect the credential file with private permissions, and avoid exposing configuration contents in shared logs or responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jordyvandomselaar/skills/radarr)
- [The Movie Database movie links](https://themoviedb.org/movie/ID)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a configured Radarr API key; commands may mutate or delete Radarr library entries.]

## Skill Version(s):

1.0.1 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
