## Description:

TencentCloud Video AIGC Detection helps agents submit videos to Tencent Cloud video moderation APIs and retrieve AI-generated video detection results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn233](https://clawhub.ai/user/shawn233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Tencent Cloud VIDEO_AIGC moderation tasks for video URLs, then query asynchronous task results for synthetic-video or deepfake detection signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends analyzed videos to Tencent Cloud services.

Mitigation: Install and use it only when sending the target videos to Tencent Cloud is acceptable for the user, organization, and use case.

Risk: The skill recommends persistent plaintext Tencent Cloud credentials in shell startup files.

Mitigation: Prefer short-lived least-privilege Tencent credentials, avoid storing static SecretKeys in shell startup files, and rotate any key that was stored that way.

Risk: Local-file handling depends on finding and installing a separate Tencent COS upload skill.

Mitigation: Use a reviewed, exact COS upload tool and confirm its configuration before submitting local files for detection.

Risk: Detection output is a Tencent moderation/AIGC signal and may not be definitive proof of authenticity.

Mitigation: Treat Pass, Review, and Block outputs as decision-support signals and apply human review where the result affects important decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shawn233/skills/tencentcloud-aigc-recog-video)
- [CreateVideoModerationTask API Reference](references/create_video_moderation_task_api.md)
- [DescribeTaskDetail API Reference](references/describe_task_detail_api.md)
- [Tencent Cloud CreateVideoModerationTask Documentation](https://cloud.tencent.com/document/product/1265/80017)
- [Tencent Cloud DescribeTaskDetail Documentation](https://cloud.tencent.com/document/product/1265/80016)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates asynchronous Tencent Cloud moderation tasks and returns task status, suggestions, labels, request IDs, and flagged snapshot or audio segment details when available.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
