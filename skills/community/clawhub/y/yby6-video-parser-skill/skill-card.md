## Description: <br>
Short Video Parser extracts metadata from short-video and image-gallery links across supported platforms and can transcribe video speech into text with SiliconFlow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangbuyiya](https://clawhub.ai/user/yangbuyiya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content operations teams use this skill to parse shared video links, collect video metadata, and generate speech transcripts or Markdown notes from processed videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video-derived audio is sent to SiliconFlow for transcription. <br>
Mitigation: Use only media that is authorized for external processing, and avoid private, confidential, or copyrighted content unless its handling has been approved. <br>
Risk: The skill fetches user-supplied video URLs from supported platforms and can use a configured external parsing API. <br>
Mitigation: Run it in an environment where outbound network access is acceptable, and provide only trusted video links and trusted parser API endpoints. <br>
Risk: Downloaded video and extracted audio may be retained locally by default. <br>
Mitigation: Enable auto_cleanup when local retention of temporary video or audio files is not desired. <br>
Risk: Credentials are needed for transcription. <br>
Mitigation: Provide API keys through runtime configuration and do not paste account cookies or secrets into source code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangbuyiya/yby6-video-parser-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yangbuyiya) <br>
- [SiliconFlow audio API documentation](https://docs.siliconflow.cn/api-reference/audio) <br>
- [SiliconFlow](https://siliconflow.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [JSON parsing results, text transcription, and generated Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and ffmpeg for transcription; transcription requires a SiliconFlow API key and may write temporary media files under tmp/ and Markdown reports under demos/.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
