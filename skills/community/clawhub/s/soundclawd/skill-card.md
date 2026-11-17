## Description:

Identify a track from a SoundCloud live set screenshot or timestamp and return Apple Music and Spotify links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjanssen19](https://clawhub.ai/user/mjanssen19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and music listeners use this skill to identify tracks playing in SoundCloud live sets, DJ mixes, or radio shows and retrieve Apple Music or Spotify links for the matched track.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Track identification may be uncertain when screenshots are unclear, cue times are missing, or the timestamp is near a transition.

Mitigation: Ask for clarification when required, state uncertainty in the response, and mention both nearby tracks when the timestamp falls near a transition.

Risk: Public tracklist and music-link sources may be blocked, incomplete, or unavailable.

Mitigation: Try the documented alternate sources, report unavailable lookups plainly, and avoid requesting credentials or bypassing access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjanssen19/skills/soundclawd)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text containing the set name, timestamp, track, artist, Apple Music link, Spotify link, and any uncertainty notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarification requests when the screenshot, timestamp, or tracklist evidence is unclear.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
