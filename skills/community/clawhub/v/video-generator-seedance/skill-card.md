## Description: <br>
Generates videos through the Volcengine SD1.5pro API, supporting text-to-video and image-to-video requests with asynchronous task processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronzoe](https://clawhub.ai/user/aaronzoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit text or image prompts to Volcengine SD1.5pro, wait for generation jobs to complete, and download the resulting MP4 video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and generated-video requests are sent to Volcengine's remote API. <br>
Mitigation: Avoid submitting confidential prompts, private image URLs, proprietary media, or regulated personal data unless authorized and comfortable with the provider's handling of that data. <br>
Risk: The skill requires a Volcengine API key in config.json. <br>
Mitigation: Store config.json carefully, keep it out of version control, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [Volcengine Console](https://console.volcengine.com/) <br>
- [Volcengine API Documentation](https://www.volcengine.com/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with bash commands; runtime output includes API status text and downloaded MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local config.json containing a Volcengine API key and model ID; generation is asynchronous and may take several minutes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
