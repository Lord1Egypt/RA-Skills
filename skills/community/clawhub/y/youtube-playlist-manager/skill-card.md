## Description:

Search YouTube, inspect video details, and manage the user's own playlists through the YouTube Data API v3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to search YouTube, inspect video details, and view or update their own playlists. Playlist access requires Google sign-in; search and video details can use an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google sign-in grants access to manage the YouTube account beyond playlists.

Mitigation: Grant access only if comfortable with the broader scope; use logout to revoke stored access.

Risk: Playlist deletion or video removal can change the user's account unexpectedly.

Mitigation: Make changes only when requested and preview delete or remove operations with dry-run.

Risk: Locally stored credentials and sign-in tokens can expose account access.

Mitigation: Keep the config and token files private to the account owner.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/odrobnik/skills/youtube-playlist-manager)
- [Publisher-listed homepage](https://github.com/odrobnik/youtube-skill)
- [YouTube IFrame Player reference](references/iframe-player.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Text or Markdown guidance; command results can also be JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and video details can use an API key; playlist commands require Google sign-in.]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
