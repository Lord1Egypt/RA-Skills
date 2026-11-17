## Description:

Clips a YouTube video locally using yt-dlp and ffmpeg, with auto-highlight detection, translation, karaoke subtitle burning, and optional Groq Whisper transcription fallback when YouTube has no subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chyyynh](https://clawhub.ai/user/chyyynh)

### License/Terms of Use:


## Use Case:

External users, developers, and creators use this skill to clip YouTube videos, select highlight segments, translate subtitles, and produce clips with optional burned-in bilingual karaoke subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Whisper fallback can send extracted audio to Groq when YouTube subtitles are unavailable and GROQ_API_KEY is set.

Mitigation: Use the skill only with non-sensitive clips unless the user has approved external transcription, or require explicit confirmation before invoking the fallback.

Risk: Video clipping depends on external tools and services, including yt-dlp, ffmpeg, YouTube subtitle availability, and expiring stream URLs.

Mitigation: Check local dependencies before use, re-resolve stream URLs after failures, and clip without subtitles or provide a transcription key when subtitles are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chyyynh/skills/video-clip-skill)
- [Publisher profile](https://clawhub.ai/user/chyyynh)
- [Groq audio transcription endpoint](https://api.groq.com/openai/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local subtitle, translation, ASS subtitle, audio, and video clip files during the workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
