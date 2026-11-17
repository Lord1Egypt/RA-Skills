## Description:

Search and add movies to Radarr, including collection support and search-on-add options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frannunpal](https://clawhub.ai/user/frannunpal)

### License/Terms of Use:


## Use Case:

External users and home media operators use this skill to search Radarr, present TMDB-linked movie results, add individual movies or collections, and remove library entries after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate a Radarr library by adding movies, adding collections, monitoring collections, and removing movies.

Mitigation: Review requested actions before execution and use a Radarr API key whose permissions are appropriate for library changes.

Risk: The remove flow can delete media files when the delete-files option is used.

Mitigation: Require explicit user confirmation before removal and separate confirmation before any file deletion.

Risk: Collection add behavior can enable monitoring and future auto-adds.

Mitigation: Confirm collection scope and monitoring behavior with the user before adding a collection.

## Reference(s):

- [Radarr Fixed ClawHub Page](https://clawhub.ai/frannunpal/skills/radarr-fixed)
- [Original Radarr Skill](https://clawhub.com/jordyvandomselaar/radarr)
- [TMDB Movie Links](https://themoviedb.org/movie/ID)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration]

**Output Format:** [Markdown guidance with shell commands and command output text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, a Radarr URL, and a Radarr API key with library mutation access.]

## Skill Version(s):

1.0.4 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
