## Description:

Spotify controls Spotify Premium playback, analyzes listening history, discovers related music, and helps create playlists through local Spotify commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mixx85](https://clawhub.ai/user/mixx85)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to control Spotify Premium playback, inspect listening history, find related music, and create or modify playlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package does not include the local spotify.py helper script that the skill instructs the agent to run.

Mitigation: Review or provide the exact local helper script before use, and confirm it matches the intended Spotify actions.

Risk: The skill can use Spotify account credentials and perform account-changing actions such as controlling playback or creating and modifying playlists.

Mitigation: Use explicit Spotify requests and confirm playlist creation, playlist modification, and other account-changing actions before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mixx85/skills/spotify-claw)
- [Project Homepage](https://github.com/mixx85/spotify-claw)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local spotify.py helper script, Spotify Premium access, Spotify app credentials, and macOS Keychain credential storage.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
