## Description: <br>
Generates short AI videos through Atlas Cloud using ByteDance Seedance models, with guidance and commands for text-to-video, image-to-video, synchronized audio, camera controls, model selection, polling, and output download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate or animate short video clips from prompts or image inputs through Atlas Cloud's hosted video generation API. It is suited for product demos, marketing clips, social media reels, cinematic scenes, and talking-head style video generation when paid API use is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script can incur paid Atlas Cloud video-generation charges. <br>
Mitigation: Use a dedicated Atlas Cloud API key, confirm the selected model and price before execution, and run only when paid generation is intended. <br>
Risk: Prompts, image URLs, video URLs, audio URLs, and uploaded local media may be sent to Atlas Cloud. <br>
Mitigation: Avoid confidential prompts and private media, and require explicit user confirmation before using the upload command or sending sensitive inputs. <br>
Risk: The helper script supports broader model and media-upload behavior than the main skill description emphasizes. <br>
Mitigation: Review generated commands for model ID, input files, URLs, and parameters before execution, especially for video-to-video, audio-guided, or upload workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/seedance-ai-video) <br>
- [Publisher profile](https://clawhub.ai/user/xixihhhh) <br>
- [Atlas Cloud](https://www.atlascloud.ai) <br>
- [Atlas Cloud video generation endpoint](https://api.atlascloud.ai/api/v1/model/generateVideo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and downloaded MP4 video files when the script is executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATLASCLOUD_API_KEY and sends prompts, image URLs, or uploaded media to Atlas Cloud.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
