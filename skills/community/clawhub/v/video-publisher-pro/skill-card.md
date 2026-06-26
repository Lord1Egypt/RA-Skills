## Description: <br>
根据IP背景和视频文案，为短视频生成一套完整的发布策略，包括发布时间、话题标签、封面文案和发布标题，并能将文案合成为封面图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and marketing teams use this skill to turn IP background, weekly goals, video scripts, and positioning into short-video publishing recommendations and cover copy. It can also guide generation of a cover image by placing the selected copy onto a user-provided background image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cover-image workflow can edit images in official-looking ways. <br>
Mitigation: Use only images and templates the user owns or is licensed to edit, and do not use the workflow to impersonate third-party official materials or remove ownership indicators. <br>
Risk: The image workflow may send user-provided images and prompts to a configurable external API. <br>
Mitigation: Confirm the exact API base URL and credential before generation, and avoid sending sensitive client material unless the destination is approved. <br>
Risk: Generated response logs may retain image-generation response content. <br>
Mitigation: Delete response logs after generation when they are no longer needed for troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/video-publisher-pro) <br>
- [Publisher profile](https://clawhub.ai/user/ahsbnb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, files] <br>
**Output Format:** [Markdown strategy report, prompt text, shell command guidance, and generated image file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include publishing-time recommendations, hashtag sets, cover copy, post titles or descriptions, and optional cover image generation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
