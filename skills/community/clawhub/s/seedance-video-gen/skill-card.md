## Description: <br>
Guides an OpenClaw agent through generating Seedance videos from text prompts, first-frame or first-and-last-frame images, reference images, draft tasks, and asynchronous task status checks using Volcengine Ark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an OpenClaw agent create AI videos with ByteDance Seedance models, manage generation tasks, and retrieve generated media. It is intended for text-to-video, image-to-video, draft preview, and task-management workflows that use a Volcengine Ark API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid Volcengine Ark/Seedance API key and can incur provider usage costs. <br>
Mitigation: Install and run only when the user is comfortable using that API key, and confirm model, duration, resolution, and draft settings before submitting generation tasks. <br>
Risk: Prompts, image URLs, and local images may be sent to Volcengine Ark for processing. <br>
Mitigation: Avoid confidential, regulated, or otherwise sensitive media unless that provider sharing is intended and approved. <br>
Risk: Task-management commands can delete or cancel generation tasks. <br>
Mitigation: Confirm task IDs before delete or cancel operations. <br>
Risk: Downloaded videos may auto-open on macOS. <br>
Mitigation: Consider disabling or avoiding auto-open behavior when reviewing untrusted or sensitive generated media. <br>


## Reference(s): <br>
- [Seedance Video ClawHub Page](https://clawhub.ai/lovensky1992-wk/seedance-video-gen) <br>
- [Seedance curl API Reference](references/curl-api-reference.md) <br>
- [Volcengine Console](https://console.volcengine.com/) <br>
- [Volcengine Ark API Base URL](https://ark.cn-beijing.volces.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands, Python CLI invocations, JSON API responses, and downloaded MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit prompts and images to Volcengine Ark, poll asynchronous task status, and download generated video files when requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
