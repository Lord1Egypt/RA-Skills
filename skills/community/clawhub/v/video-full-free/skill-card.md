## Description:

Builds a short-form AI video pipeline that turns a topic into a scene script, generates scene videos with Wan on HuggingFace, creates voiceover with ElevenLabs, merges media with FFmpeg, and sends the final video to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eslamshtain11](https://clawhub.ai/user/eslamshtain11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users can use this skill to assemble an AI-assisted workflow for creating 60-90 second vertical videos from a topic, including script generation, scene media, Arabic-capable voiceover, FFmpeg composition, and Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated content can be sent automatically to Telegram and external services without a clear per-run confirmation step.

Mitigation: Confirm the Telegram chat destination and require explicit approval before sending generated media.

Risk: Topics, scripts, prompts, and voiceover text may be shared with third-party APIs.

Mitigation: Avoid confidential topics or scripts and review generated text before calling external services.

Risk: A project_name derived from user input can affect local output paths.

Mitigation: Restrict project_name to a simple safe identifier before creating folders or media files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eslamshtain11/skills/video-full-free)
- [Wan2.6 API Reference](references/wan2-api.md)
- [ElevenLabs Arabic Settings](references/elevenlabs-arabic.md)
- [FFmpeg Recipes](references/ffmpeg-recipes.md)
- [HuggingFace Wan2.6 inference endpoint](https://api-inference.huggingface.co/models/Wan-AI/Wan2.6-T2V-14B)
- [ElevenLabs text-to-speech API](https://api.elevenlabs.io/v1/text-to-speech/{voice_id})
- [Telegram sendVideo API](https://api.telegram.org/bot{bot_token}/sendVideo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON schemas, Python code examples, environment variables, and FFmpeg shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instructions for generating video, audio, merged MP4 files, captions, and Telegram delivery calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
