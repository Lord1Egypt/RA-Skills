## Description: <br>
Use the RenderIO FFmpeg-as-a-Service API to process video, audio, and images in the cloud, including submitting commands, polling results, uploading files, chained workflows, and webhook delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nevermind-s](https://clawhub.ai/user/nevermind-s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate RenderIO API requests and example code for cloud FFmpeg media-processing workflows such as conversion, resizing, compression, trimming, watermarking, audio extraction, uploads, chained jobs, and webhook delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RenderIO API key. <br>
Mitigation: Store RENDERIO_API_KEY in an environment variable or secret manager, and do not paste it into chats, generated files, or source control. <br>
Risk: Media files and signed output URLs are handled by a third-party cloud processor. <br>
Mitigation: Upload only media you are authorized to send to RenderIO, and treat returned signed output URLs as sensitive access links. <br>
Risk: Using the wrong RenderIO API hostname can break workflows or send requests to an unintended endpoint. <br>
Mitigation: Confirm the current RenderIO API hostname from official RenderIO documentation before installing or running generated commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nevermind-s/renderio-ffmpeg-api) <br>
- [RenderIO API key page](https://renderio.dev/get-api-key) <br>
- [RenderIO FFmpeg command endpoint](https://renderio.dev/api/v1/run-ffmpeg-command) <br>
- [RenderIO file upload endpoint](https://renderio.dev/api/v1/files/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, TypeScript, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API request patterns, polling guidance, upload guidance, webhook setup examples, and media-processing recipes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
