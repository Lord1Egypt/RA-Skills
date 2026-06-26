## Description: <br>
Generate videos using SiliconFlow API with Wan2.2 model. Supports both Text-to-Video and Image-to-Video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to submit text-to-video or image-to-video generation jobs to SiliconFlow and receive an asynchronous request identifier for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and the SiliconFlow API key are sent to SiliconFlow when the skill submits a generation job. <br>
Mitigation: Use a dedicated SiliconFlow API key with limited billing exposure and review the OpenClaw configuration so only the intended credential is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/siliconflow-video-gen) <br>
- [Publisher profile](https://clawhub.ai/user/lilei0311) <br>
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status messages and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits asynchronous video generation jobs and returns a request_id rather than the generated video file.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
