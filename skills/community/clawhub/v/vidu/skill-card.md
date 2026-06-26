## Description: <br>
Generate AI videos using Vidu with text-to-video, image-to-video, reference-to-video, and start-end-to-video workflows across Vidu Q3-Pro and Vidu 2.0 models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and marketing teams use this skill to generate short AI video clips, animate images, interpolate between keyframes, and create character-consistent videos through Atlas Cloud's Vidu endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Atlas Cloud API usage can incur paid video-generation charges. <br>
Mitigation: Confirm user intent before generation, monitor account spending, and choose draft settings such as lower resolution when appropriate. <br>
Risk: Prompts, image URLs, uploaded media, video data, or likenesses may be processed by Atlas Cloud. <br>
Mitigation: Avoid sending confidential, private, rights-sensitive, or unauthorized media unless the user is comfortable with Atlas Cloud processing. <br>
Risk: The ATLASCLOUD_API_KEY grants access to models available on the user's Atlas Cloud account. <br>
Mitigation: Store the key only in the environment, avoid logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/vidu) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>
- [fal.ai Vidu Q3-Pro text-to-video pricing reference](https://fal.ai/models/fal-ai/vidu/q3-pro/text-to-video) <br>
- [Atlas Cloud video generation API endpoint](https://api.atlascloud.ai/api/v1/model/generateVideo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, Python script usage examples, API request examples, and downloaded MP4 video files when generation succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY and sends prompts, image URLs, uploaded media, and generation requests to Atlas Cloud.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
