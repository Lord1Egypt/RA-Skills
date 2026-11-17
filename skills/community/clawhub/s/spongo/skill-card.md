## Description:

Terminal Spotify playback/search via spogo (preferred) or spotify_player.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nabssku](https://clawhub.ai/user/nabssku)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control Spotify playback and search from a terminal through spogo or spotify_player.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The spogo setup can import Chrome cookies for Spotify authentication, which may expose sensitive browser session data depending on how the external tool stores credentials.

Mitigation: Review the authentication flow before use, prefer spotify_player or another flow that does not read browser cookies when appropriate, and use a dedicated browser profile or session if importing cookies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nabssku/skills/spongo)
- [Spotify](https://www.spotify.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Spotify Premium and either spogo or spotify_player installed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
