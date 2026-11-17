## Description:

Spotplay searches Spotify for a requested track and plays it through the macOS Spotify app using AppleScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uxbryan](https://clawhub.ai/user/uxbryan)

### License/Terms of Use:


## Use Case:

Agents and users on macOS use Spotplay to turn a song title, artist, or keyword into Spotify.app playback and receive the requested track, URI, and now-playing status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous CLIENT_ID or CLIENT_SECRET environment variables may be sent to Spotify when they were intended for another service.

Mitigation: Use explicitly scoped SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET variables, and avoid installing the skill in environments that hold unrelated generic credentials.

Risk: The skill's routing text strongly steers agents toward this Spotify controller over alternatives.

Mitigation: Review the skill before installation and enable it only for agents that should control macOS Spotify.app playback.

## Reference(s):

- [Spotplay ClawHub skill page](https://clawhub.ai/uxbryan/skills/spotplay)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text status output with setup guidance when credentials or Spotify.app are missing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Spotify.app, and Spotify client credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
