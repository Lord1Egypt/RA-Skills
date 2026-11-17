## Description:

Generates and processes speech, music, video, and images using MiniMax APIs and FFmpeg-based media tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhlorra](https://clawhub.ai/user/yhlorra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan and run MiniMax media generation workflows for TTS, voice cloning, music, image, video, long-form video, templates, and local media processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can send MiniMax API keys and uploaded media to a nonstandard API host.

Mitigation: Set MINIMAX_API_HOST only to https://api.minimaxi.com or https://api.minimax.io, inspect project .env files before use, and avoid optional API tests or generation scripts when the host is nonstandard.

Risk: Generation workflows require a MiniMax API key in the local environment or .env files.

Mitigation: Use an appropriate MiniMax key, avoid sharing .env files, and rotate the key if the scripts were run with an unexpected host.

Risk: Prompts and local media files may be uploaded to MiniMax API endpoints during generation or voice cloning.

Mitigation: Confirm the selected endpoint and avoid uploading confidential, restricted, or unapproved media unless the account and region are approved for that use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yhlorra/skills/yh-minimax-multimodal-toolkit)
- [MiniMax China Platform](https://platform.minimaxi.com)
- [MiniMax Global Platform](https://platform.minimax.io)
- [MiniMax Image Generation API](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i)
- [MiniMax Image-to-Image API](https://platform.minimaxi.com/docs/api-reference/image-generation-i2i)
- [Image API Reference](references/image-api.md)
- [Music API Reference](references/music-api.md)
- [TTS Guide](references/tts-guide.md)
- [TTS Voice Catalog](references/tts-voice-catalog.md)
- [Video API Reference](references/video-api.md)
- [Video Prompt Writing Guide](references/video-prompt-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON snippets, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is saved under minimax-output/; API calls require MINIMAX_API_HOST and MINIMAX_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
