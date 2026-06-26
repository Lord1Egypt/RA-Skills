## Description: <br>
Use RunningHub official standard-model APIs to generate image-to-video outputs, upload local source images when needed, poll task status, and download completed videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darker314159](https://clawhub.ai/user/darker314159) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run RunningHub image-to-video jobs from public URLs or local source images, monitor task progress, and retrieve generated media files. It is suited for workflows that need model-specific endpoint guidance and local download of completed video outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected images, prompts, and API-authenticated requests to RunningHub for external processing. <br>
Mitigation: Use it only when external processing is acceptable, avoid sensitive images, and prefer the RUNNINGHUB_API_KEY environment variable instead of passing credentials on the command line. <br>
Risk: Generated outputs and uploaded media links may expire after task completion. <br>
Mitigation: Use a dedicated output directory and download completed media promptly after polling reports success. <br>


## Reference(s): <br>
- [RunningHub Video API Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/darker314159/runninghub-video) <br>
- [RunningHub API Base](https://www.runninghub.cn) <br>
- [RunningHub Media Upload Endpoint](https://www.runninghub.cn/openapi/v2/media/upload/binary) <br>
- [RunningHub Task Query Endpoint](https://www.runninghub.cn/openapi/v2/query) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown with command examples, JSON task status summaries, and local media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload selected images and prompts to RunningHub, then save generated video outputs to a user-selected local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
