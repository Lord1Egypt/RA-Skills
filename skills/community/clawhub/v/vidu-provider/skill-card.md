## Description: <br>
Video generation provider plugin for Vidu (viduq3-pro, viduq3-turbo, viduq2, viduq1). Supports text-to-video, image-to-video, reference-to-video, and start-end-to-video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaonan-ss](https://clawhub.ai/user/xiaonan-ss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect agents to Vidu for text-to-video, image-to-video, reference-to-video, and start-end video generation with a configured Vidu API key. <br>

### Deployment Geography for Use: <br>
Global; the plugin supports both global and China Vidu API endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts, uploaded images, and uploaded videos are sent to Vidu for generation. <br>
Mitigation: Install only when this data sharing is acceptable for the intended users and workload. <br>
Risk: The Vidu API key is a sensitive credential. <br>
Mitigation: Store VIDU_API_KEY as a secret and rotate it if it is exposed. <br>
Risk: The provider is enabled by default and applies a default video generation model during onboarding. <br>
Mitigation: Review default-provider and default-model behavior if the OpenClaw deployment requires stricter manual activation. <br>


## Reference(s): <br>
- [Vidu Platform](https://platform.vidu.com) <br>
- [ClawHub release page](https://clawhub.ai/xiaonan-ss/vidu-provider) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Configuration] <br>
**Output Format:** [Generated video files with provider metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VIDU_API_KEY, supports one generated video per request, and can use text, image, video, and start/end-frame inputs depending on the selected Vidu model.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
