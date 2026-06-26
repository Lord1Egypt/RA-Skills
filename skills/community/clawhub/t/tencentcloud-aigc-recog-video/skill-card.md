## Description: <br>
TencentCloud Video AIGC Detection helps agents submit videos to Tencent Cloud VIDEO_AIGC moderation and report whether the service labels them as AI-generated, suspicious, or normal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn233](https://clawhub.ai/user/shawn233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content moderation teams, and agents use this skill to create Tencent Cloud AI-generated-video detection tasks, poll asynchronous results, and present Tencent Cloud suggestions for video authenticity review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local-video workflows can upload private files through a separate COS upload step before detection. <br>
Mitigation: Use URL input where possible, approve any COS upload explicitly, verify the upload skill before installation, and send only media appropriate for Tencent Cloud processing. <br>
Risk: The skill requires Tencent Cloud API credentials and a BizType to call the video moderation service. <br>
Mitigation: Use least-privilege or temporary Tencent Cloud credentials, avoid hardcoding secrets, and configure only credentials needed for the intended media review workflow. <br>


## Reference(s): <br>
- [CreateVideoModerationTask API reference](references/create_video_moderation_task_api.md) <br>
- [DescribeTaskDetail API reference](references/describe_task_detail_api.md) <br>
- [Tencent Cloud CreateVideoModerationTask documentation](https://cloud.tencent.com/document/product/1265/80017) <br>
- [Tencent Cloud DescribeTaskDetail documentation](https://cloud.tencent.com/document/product/1265/80016) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates asynchronous Tencent Cloud moderation tasks and reports status, suggestion, labels, confidence scores, and request identifiers from API responses.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
