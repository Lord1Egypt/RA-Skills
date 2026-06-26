## Description: <br>
Generate and process speech, music, video, and images using MiniMax AI with voice cloning, custom voices, multi-scene video, and FFmpeg-based media tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhlorra](https://clawhub.ai/user/yhlorra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to call MiniMax APIs for text-to-speech, voice cloning, music generation, image generation, video generation, and media processing workflows from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, images, videos, and voice samples are sent to MiniMax services. <br>
Mitigation: Avoid confidential or sensitive content unless the user has reviewed the data-sharing implications and MiniMax service terms. <br>
Risk: Voice cloning and face-reference workflows can be misused without consent. <br>
Mitigation: Use only voice samples and face references where the user has appropriate permission and a legitimate use case. <br>
Risk: The skill relies on a MiniMax API key and user-selected API host. <br>
Mitigation: Store the API key in a safer secret store or temporary environment and keep MINIMAX_API_HOST set only to documented MiniMax endpoints. <br>
Risk: Generated output paths may overwrite existing files. <br>
Mitigation: Choose output paths deliberately, keep generated assets under minimax-output/, and review files before reuse or publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yhlorra/yh-minimax-multimodal-toolkit) <br>
- [MiniMax Multimodal Toolkit](SKILL.md) <br>
- [TTS Guide](references/tts-guide.md) <br>
- [TTS Voice Catalog](references/tts-voice-catalog.md) <br>
- [MiniMax Music Generation API](references/music-api.md) <br>
- [MiniMax Image Generation API](references/image-api.md) <br>
- [MiniMax Video Generation API](references/video-api.md) <br>
- [Video Prompt Guide](references/video-prompt-guide.md) <br>
- [MiniMax image generation documentation](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i) <br>
- [MiniMax music generation documentation](https://platform.minimaxi.com/docs/api-reference/music-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets are directed to minimax-output/ and may include audio, image, video, JSON, and intermediate media files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
