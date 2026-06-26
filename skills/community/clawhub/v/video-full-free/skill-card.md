## Description: <br>
Generates a 60-90 second short-video workflow from a topic by drafting scene scripts, creating scene video with Wan2.6, generating voiceover with ElevenLabs, merging media with FFmpeg, and sending the final video through Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eslamshtain11](https://clawhub.ai/user/eslamshtain11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to assemble an automated short-form video pipeline that turns a topic into scene prompts, narration, merged video files, and Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generated scripts, narration text, media, and final videos are sent to third-party services including Hugging Face, ElevenLabs, and Telegram. <br>
Mitigation: Use dedicated revocable API keys, avoid private or regulated content, and review generated media and Telegram destinations before sending. <br>
Risk: Voice cloning or synthetic narration can create consent and impersonation concerns. <br>
Mitigation: Use voice cloning only with explicit speaker permission and select authorized voices for production workflows. <br>
Risk: Automated Telegram delivery can send generated video to the wrong recipient if the chat ID is misconfigured. <br>
Mitigation: Confirm the Telegram chat ID and destination before running the delivery step. <br>


## Reference(s): <br>
- [Wan2.6 API Reference](references/wan2-api.md) <br>
- [ElevenLabs Arabic Voice Settings](references/elevenlabs-arabic.md) <br>
- [FFmpeg Short-Video Recipes](references/ffmpeg-recipes.md) <br>
- [Hugging Face Wan2.6 Inference Endpoint](https://api-inference.huggingface.co/models/Wan-AI/Wan2.6-T2V-14B) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow instructions and code samples for generating MP4 scene files, MP3 voiceover files, merged video files, and Telegram delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
