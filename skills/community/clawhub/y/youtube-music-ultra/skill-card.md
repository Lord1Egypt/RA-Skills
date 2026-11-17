## Description:

Control YouTube Music with natural language commands for playback, search, direct video ID playback, and browser-based media control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oki3505f](https://clawhub.ai/user/oki3505f)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to control YouTube Music from an OpenClaw browser profile through natural language or shell commands. It is intended for playback, search, direct video ID playback, and basic media control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls an OpenClaw browser profile for YouTube Music.

Mitigation: Use an isolated browser profile and account for this skill instead of a primary personal profile.

Risk: Commands may be unsafe when given untrusted text or URLs.

Mitigation: Pass only trusted song queries, video IDs, and URLs until command construction is reviewed and fixed.

Risk: Persistent temporary cache handling is weak.

Mitigation: Clear the skill's /tmp cache files when needed and avoid relying on cached entries for sensitive or shared environments.

Risk: Documentation overstates playlist, queue, lyrics, and recommendation capabilities.

Mitigation: Treat those features as unreliable until the scripts and documentation are aligned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oki3505f/skills/youtube-music-ultra)
- [Publisher profile](https://clawhub.ai/user/oki3505f)
- [YouTube Music](https://music.youtube.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and browser-control instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate against a local OpenClaw browser profile and may use temporary cache files.]

## Skill Version(s):

3.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
