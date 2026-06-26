## Description: <br>
Generate videos from image and text prompts using the Tomoviee Image-to-Video API through the Wondershare OpenAPI gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn a source image URL and motion prompt into a short generated video via Tomoviee/Wondershare APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs, prompts, and optional callback data are sent to Tomoviee/Wondershare services. <br>
Mitigation: Use the skill only with data that is appropriate to send to that provider and review callback payload handling before enabling callbacks. <br>
Risk: App keys, app secrets, and generated Basic tokens can grant API access if exposed. <br>
Mitigation: Keep credentials out of shared terminals, shell history, repositories, and CI logs; treat printed tokens as secrets. <br>
Risk: Callback URLs may expose generated task data to an endpoint outside the user's control. <br>
Mitigation: Configure callbacks only to endpoints the user controls and monitors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/tomoviee-image-to-video) <br>
- [Tomoviee API docs](https://www.tomoviee.ai/doc/ai-video/image-to-video.html) <br>
- [Tomoviee developer portal](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee Image-to-Video API Reference](references/video_apis.md) <br>
- [Camera Movement Types Reference](references/camera_movements.md) <br>
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API task identifiers and polling guidance for retrieving generated video URLs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
