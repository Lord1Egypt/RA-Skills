## Description:

Downloads social video links with yt-dlp, either saving the best available video file or preparing downloaded media and transcripts for reusable skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olliewazza](https://clawhub.ai/user/olliewazza)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download social media videos in best available quality and, when needed, generate transcripts that can support concise OpenClaw skill creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcription mode can send extracted audio to OpenAI when OPENAI_API_KEY is present, creating privacy and billing implications.

Mitigation: Use transcription only for authorized videos, run it in a private output directory, and unset OPENAI_API_KEY unless sending audio to OpenAI is intended.

Risk: Some social sites may require login, cookies, or permission to access media.

Mitigation: Use only URLs the user is authorized to download, and ask before using a logged-in browser session or cookies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/olliewazza/skills/social-downloader)
- [OpenAI audio transcriptions API endpoint](https://api.openai.com/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Text, Guidance]

**Output Format:** [Markdown guidance with shell commands; scripts produce media files, result JSON, and optional transcript text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create downloaded video and audio files in a local output directory; transcription sends audio to OpenAI only when OPENAI_API_KEY is set.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
