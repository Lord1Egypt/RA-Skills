## Description:

Control Tidal music streaming from the terminal for catalog search, playlist management, library and favorites changes, playback, recommendations, and user profile lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaperret](https://clawhub.ai/user/lucaperret)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent operate Tidal through the tidal-cli command line tool, including searching music, managing playlists and library items, and retrieving playback or recommendation data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party CLI package.

Mitigation: Review the npm package source before installation and pin or verify the package version in controlled environments.

Risk: The CLI stores a persistent Tidal session at ~/.tidal-cli/session.json.

Mitigation: Treat the session file as sensitive account material and protect access on shared machines.

Risk: Playlist and library commands can delete, remove, rename, or otherwise change user content.

Mitigation: Confirm exact playlist, track, album, artist, or library targets before running destructive or mutating commands.

## Reference(s):

- [Tidal CLI npm package](https://www.npmjs.com/package/@lucaperret/tidal-cli)
- [ClawHub skill page](https://clawhub.ai/lucaperret/skills/tidal-cli)
- [Publisher profile](https://clawhub.ai/user/lucaperret)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses tidal-cli with --json for programmatic responses when available.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
