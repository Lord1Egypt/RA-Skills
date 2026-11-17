## Description:

Access your Vibo (vibodj.com) event music planning via MCP. Use when the user asks about their Vibo events, wedding/event timeline, song requests, playlists, or "do not play" list, or wants to add or like songs, join an event from a share link, or export songs to Spotify/Apple Music. Triggers on phrases like "what's on my Vibo timeline", "add this song to the first dance", "what songs did guests request", "join this Vibo event", or "export our playlist to Spotify". Requires vibo-mcp installed and the vibo server registered (see Setup below).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Event hosts, couples, and guests use this skill to review Vibo event timelines, song requests, playlists, and DJ planning details, and to manage music and event information through Vibo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis is incomplete because some referenced material was unavailable for review.

Mitigation: Review the complete skill and consider whether its stated purpose is trusted before installing.

Risk: The skill can make changes to shared event and music information.

Mitigation: Review the confirmation preview and approve the specific change before the write is sent.

## Reference(s):

- [Vibo](https://vibodj.com)
- [vibo-mcp on npm](https://www.npmjs.com/package/vibo-mcp)
- [vibo-mcp project page (linked in the skill artifact)](https://github.com/chrischall/vibo-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration instructions]

**Output Format:** [Natural-language responses and structured Vibo event, timeline, and song data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can initiate event and music changes; write operations use confirmation previews.]

## Skill Version(s):

2.6.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
