## Description:

AI skill to analyze song requests, verify local workspace files, and download missing tracks directly from YouTube bypassing API limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhathuynguyen19](https://clawhub.ai/user/nhathuynguyen19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify requested music tracks, check the OpenClaw workspace for existing files, and download missing audio for local playback through cmus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted song title or artist string could cause unintended local shell command behavior when used in find or yt-dlp commands.

Mitigation: Treat song titles and artists as untrusted input, ask before downloading, and execute commands with safely separated arguments or robust escaping.

Risk: Downloads depend on externally installed yt-dlp and ffmpeg tools.

Mitigation: Install dependencies from controlled sources and pin or otherwise control the yt-dlp package source when reproducible installs are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nhathuynguyen19/skills/yt-dlp-cmus)
- [yt-dlp project homepage](https://github.com/yt-dlp/yt-dlp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local MP3 audio files in ~/.openclaw/workspace/music/ when the agent executes the recommended workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
