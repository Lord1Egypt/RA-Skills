## Description:

Control YouTube Music through OpenClaw browser automation with natural-language playback, search, queue, playlist, lyrics, and direct video ID commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oki3505f](https://clawhub.ai/user/oki3505f)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to control YouTube Music from an OpenClaw agent, including play, pause, skip, search, volume, queue, playlist, lyrics, and direct video ID workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted play, search, or direct-video inputs may reach shell command strings used by browser-control scripts.

Mitigation: Use argument-array process execution and strictly validate YouTube URLs, video IDs, and search text before invoking browser commands.

Risk: Broad natural-language activation can trigger unintended playback, search, playlist, or browser actions.

Mitigation: Use clearer activation rules and require confirmation for ambiguous or state-changing music commands.

Risk: Shared cache files under /tmp can expose or allow tampering with cached playback/search state on multi-user systems.

Mitigation: Store cache data in a private per-user directory with restrictive permissions, validate cache contents before use, and expire stale entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oki3505f/skills/youtube-music)
- [YouTube Music web app](https://music.youtube.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and natural-language command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Controls a browser session through OpenClaw; requires node and the YOUTUBE_MUSIC_BROWSER_PROFILE environment setting.]

## Skill Version(s):

3.0.0 (source: server release metadata and package.json; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
