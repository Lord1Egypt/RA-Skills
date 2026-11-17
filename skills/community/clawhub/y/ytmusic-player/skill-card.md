## Description:

Operate YouTube Music via natural language to search songs, artists, albums, playlists, lyrics, charts, and recommendations; browse a personal library; manage playlists; rate tracks; inspect account information; and control playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadaliao](https://clawhub.ai/user/kadaliao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search YouTube Music, control playback, and manage personal library or playlist workflows. The skill is useful when a user wants concise music results, lyrics, account-aware library actions, or playback status from YouTube Music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable YouTube or Google session cookies and stores API auth headers under .ytmusic/auth.json.

Mitigation: Use a dedicated low-risk account, avoid pasting cookies into chat when possible, restrict access to the local runtime directory, and remove stored auth with the provided auth remove command when done.

Risk: Playback uses a persistent Playwright browser profile and daemon state under .ytmusic, which can preserve an authenticated browser session.

Mitigation: Stop the daemon when playback is no longer needed and clear the dedicated browser profile if the session should not persist.

Risk: Authenticated commands can change user-visible YouTube Music state, including playlists, ratings, subscriptions, history, uploads, and playback.

Mitigation: Confirm user intent before destructive or account-changing actions, especially playlist deletion, history removal, uploads, and subscription changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadaliao/skills/ytmusic-player)
- [Publisher profile](https://clawhub.ai/user/kadaliao)
- [Project homepage](https://github.com/kadaliao/ytmusic-skill)
- [YouTube Music command reference](references/commands.md)
- [YouTube Music](https://music.youtube.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and summarized JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are formatted as short tables or lists; lyrics are plain text; playback returns status text; authenticated actions require local YouTube Music session data.]

## Skill Version(s):

0.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
