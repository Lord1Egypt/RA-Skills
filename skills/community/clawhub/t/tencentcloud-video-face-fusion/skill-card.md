## Description: <br>
This skill submits and monitors Tencent Cloud video face fusion jobs that merge user face images into template videos for creative marketing, entertainment, and social sharing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neck-cn](https://clawhub.ai/user/Neck-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit, poll, and query Tencent Cloud video face fusion jobs when a user provides a template video, template face image, and replacement face image. It is intended for workflows that generate face-fused video outputs through Tencent Cloud rather than synthesizing results locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected face images and video material to Tencent Cloud for processing. <br>
Mitigation: Use it only with consent for the people whose faces are processed and only when the account owner accepts Tencent Cloud processing of that media. <br>
Risk: The scripts use Tencent Cloud credentials and may submit jobs automatically once invoked. <br>
Mitigation: Use least-privileged Tencent Cloud credentials, keep them out of source files and long-lived shell profiles where possible, and run the skill in an isolated Python environment. <br>
Risk: Generated or modified face-fusion videos can be misused or mistaken for authentic media. <br>
Mitigation: Keep the AI synthesis label enabled unless there is a reviewed reason to disable it, and review outputs before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Neck-cn/tencentcloud-video-face-fusion) <br>
- [Submit Video Face Fusion API reference](references/submit_video_face_fusion_api.md) <br>
- [Describe Video Face Fusion API reference](references/describe_video_face_fusion_api.md) <br>
- [Tencent Cloud Video Creation console](https://console.cloud.tencent.com/vclm) <br>
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status or result responses from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a Tencent Cloud job ID, request ID, task status, error details, or a result video URL when processing completes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
