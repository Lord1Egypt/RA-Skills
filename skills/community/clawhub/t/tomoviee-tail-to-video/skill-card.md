## Description: <br>
Generate videos from first and last frame images using Tomoviee First-Last Frame API (`tm_tail2video_b`) via Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation users use this skill to generate a fixed 5-second video by interpolating between a first-frame image URL and a last-frame image URL with prompt guidance. It is scoped to the Tomoviee `tm_tail2video_b` first-last-frame workflow and requires Tomoviee app credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials or generated Basic auth tokens may be exposed if entered as command-line arguments or printed in shared terminals and logs. <br>
Mitigation: Use environment variables or an interactive secret prompt for `app_key` and `app_secret`, avoid shared shells and CI logs, and do not store generated tokens. <br>
Risk: Private, signed, localhost, or internal media and callback URLs could be sent to the third-party Tomoviee/Wondershare API. <br>
Mitigation: Use only public media URLs intended for third-party processing and avoid internal or sensitive callback endpoints. <br>
Risk: Included Tomoviee reference material covers broader video workflows than this skill implements. <br>
Mitigation: Constrain use to the documented `tm_tail2video_b` first-last-frame workflow and review prompts, parameters, and endpoints before deployment. <br>


## Reference(s): <br>
- [Tomoviee First-Last Frame to Video API Reference](references/video_apis.md) <br>
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md) <br>
- [Camera Movement Types Reference](references/camera_movements.md) <br>
- [Tomoviee developer portal](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee first-last-frame API documentation](https://www.tomoviee.ai/doc/ai-video/first-and-last-frame-to-video.html) <br>
- [Tomoviee mainland developer portal](https://www.tomoviee.cn/developers.html) <br>
- [Tomoviee mainland first-last-frame API documentation](https://www.tomoviee.cn/doc/ai-video/first-and-last-frame-to-video.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash snippets; API calls return task metadata and result JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or retrieves a video URL from the Tomoviee result payload after asynchronous polling.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
