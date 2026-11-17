## Description:

Create Twitch clips of the current live stream via the Twitch API. Use when a streamer says "clip that", "clip the last X seconds", "make a clip", "clip it", or any variation requesting a clip of the current broadcast. Requires Twitch API credentials configured in environment variables. Has a 30-second cooldown between clips to prevent spam.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Streamers and their assistants use this skill to create a clip from a live Twitch broadcast and share the resulting clip link. It is intended for explicit clip requests and requires Twitch API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the script immediately attempts to create a public Twitch clip.

Mitigation: Run it only for an explicit clip request and confirm the request before invoking the script.

Risk: The Twitch access token grants clip-creation authority and could be exposed if mishandled.

Mitigation: Use a token limited to the documented clips:edit scope and keep it private.

## Reference(s):

- [Twitch Clip skill release](https://clawhub.ai/djc00p/skills/twitch-clip)
- [Twitch Developer Console](https://dev.twitch.tv/console/apps)
- [Twitch Helix Users API](https://api.twitch.tv/helix/users)
- [Twitch Clips API endpoint](https://api.twitch.tv/helix/clips)

## Skill Output:

**Output Type(s):** [Text, URLs, Shell commands]

**Output Format:** [Plain text status messages and a Twitch clip URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Clip duration from 5 to 60 seconds (30 seconds by default); 30-second cooldown between clips.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
