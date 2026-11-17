## Description:

TencentCloud Video Effects turns a user-provided image and selected effect template into an animated special-effects video through Tencent Cloud's TemplateToVideo service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neck-cn](https://clawhub.ai/user/neck-cn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to submit a person image and video effect template to Tencent Cloud, then return either the generated video URL or a job ID for later retrieval. It is useful when a workflow needs to transform static images into short animated effects videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected images to Tencent Cloud without a separate confirmation step.

Mitigation: Use it only for images approved for Tencent Cloud processing and make that data-sharing expectation clear in the agent workflow.

Risk: Tencent Cloud credentials are exposed to the skill process.

Mitigation: Use least-privileged Tencent Cloud credentials, keep them in environment variables or a managed secret store, and rotate them according to local policy.

Risk: The script can automatically install unpinned Tencent Cloud SDK code at runtime.

Mitigation: Preinstall and pin required dependencies in a controlled environment and avoid relying on the automatic install path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neck-cn/skills/tencentcloud-video-effects)
- [Publisher Profile](https://clawhub.ai/user/neck-cn)
- [SubmitTemplateToVideoJob Reference](references/SubmitTemplateToVideoJob.md)
- [DescribeTemplateToVideoJob Reference](references/DescribeTemplateToVideoJob.md)
- [Tencent Cloud SubmitTemplateToVideoJob Documentation](https://cloud.tencent.com/document/product/1616/119001)
- [Tencent Cloud DescribeTemplateToVideoJob Documentation](https://cloud.tencent.com/document/product/1616/119002)
- [Tencent Cloud Video Effects Console](https://console.cloud.tencent.com/vtc/creation/video-special)
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON response containing a generated video URL, a job ID, or structured error details; setup guidance may include Markdown with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous Tencent Cloud video jobs and can either poll until completion or return only the submitted JobId.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
