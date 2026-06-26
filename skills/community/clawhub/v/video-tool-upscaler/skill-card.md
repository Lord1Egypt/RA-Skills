## Description: <br>
Upscale an existing HTTPS video via WeryAI (video-upscaler). Use when the user wants higher resolution output, not text-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to upscale an existing public HTTPS video through WeryAI, choosing 1080p, 2k, or 4k output. It is for higher-resolution processing of an existing video, not text-to-video or image-to-video generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends the selected public video URL to WeryAI and requires WERYAI_API_KEY. <br>
Mitigation: Use the skill only for videos that may be processed by WeryAI, keep the API key in the environment, and do not write the key into files or prompts. <br>
Risk: Submitting or waiting on an upscale job may consume paid WeryAI credits. <br>
Mitigation: Run dry-run validation first and require explicit user confirmation of the video URL and any non-default resolution before submit or wait. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-upscaler) <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with shell commands and final video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and a public HTTPS video URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
