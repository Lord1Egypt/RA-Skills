## Description:

One-command YouTube video transcription that automatically downloads audio and transcribes using the OpenAI Whisper API when YouTube subtitles are disabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edisonchenai](https://clawhub.ai/user/edisonchenai)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to produce transcripts for YouTube videos, including cases where captions are unavailable. It can fetch existing subtitles first and fall back to audio download plus OpenAI Whisper transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling can let a crafted output filename run local code or overwrite files.

Mitigation: Review or fix the shell script before deployment and avoid untrusted or unusual --out paths.

Risk: Fallback transcription sends downloaded audio to OpenAI Whisper.

Mitigation: Do not run the skill on sensitive videos unless sending audio to OpenAI is acceptable for the user's environment.

Risk: The skill depends on local yt-dlp and ffmpeg installations.

Mitigation: Use pinned, verified dependency installs and keep yt-dlp updated when YouTube access fails.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/edisonchenai/skills/youtube-transcriber)
- [Claude Code](https://claude.com/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript file with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcripts to a user-specified path or a default /tmp path; may call OpenAI Whisper API when subtitles are unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
