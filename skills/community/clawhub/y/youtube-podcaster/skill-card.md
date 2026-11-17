## Description:

Extracts YouTube video text and converts it into a multi-voice AI podcast using Gemini for script generation, OpenAI TTS, a local Node.js API, and FFmpeg, with WebVTT output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaudata](https://clawhub.ai/user/kaudata)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn YouTube videos into multi-host podcast assets, including the original transcript, generated script, M4A audio, WebVTT captions, and downloadable bundles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web app stores generated transcript, script, caption, and audio files and exposes them through local download routes.

Mitigation: Run the server only on trusted local machines, keep the localhost binding, delete session folders after use, and avoid processing sensitive content unless local storage is acceptable.

Risk: The security evidence reports overly broad generated-file access and destructive cleanup behavior.

Mitigation: Use predictable, private sessions only in trusted environments; before broad use, add strict session ID validation, session authorization, and safer delete behavior.

Risk: The security evidence reports exploitable handling of AI-produced content in the local web app.

Mitigation: Review generated search, caption, and script content before use; replace unsafe browser rendering with safe text or DOM construction before broad deployment.

Risk: Transcript and script content is sent to Gemini and OpenAI, and API keys are required for normal operation.

Mitigation: Use only content permitted by the user's data-handling policy, protect API keys in the local environment, and rotate keys if they may have been exposed.

Risk: Long-running audio generation and FFmpeg processing may consume local resources, and the security guidance notes missing server timeouts.

Mitigation: Generate bounded workloads, stop the tracked server process after use, and add server timeouts before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaudata/skills/youtube-podcaster)
- [Publisher profile](https://clawhub.ai/user/kaudata)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance plus local text, WebVTT, M4A audio, and ZIP files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, ffmpeg, curl, GEMINI_API_KEY, and OPENAI_API_KEY; generated files are stored under a local downloads session folder.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
