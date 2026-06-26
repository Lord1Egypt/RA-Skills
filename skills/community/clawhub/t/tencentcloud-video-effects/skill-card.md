## Description: <br>
Generates a video-effects result from an image and a selected Tencent Cloud template, turning a static image into a dynamic video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neck-cn](https://clawhub.ai/user/Neck-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to submit image-to-video effects jobs to Tencent Cloud, optionally poll for completion, and return the generated video URL or job identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload selected local images or image URLs to Tencent Cloud. <br>
Mitigation: Use explicit user confirmation for sensitive images and run with only images intended for Tencent Cloud processing. <br>
Risk: Tencent Cloud credentials are required in the execution environment. <br>
Mitigation: Use narrowly scoped credentials and avoid hard-coding secrets in code or prompts. <br>
Risk: The script can install the Tencent Cloud Python SDK at runtime if it is missing. <br>
Mitigation: Prefer an isolated environment with a pinned, preinstalled SDK before running the skill. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Neck-cn/tencentcloud-video-effects) <br>
- [SubmitTemplateToVideoJob reference](references/SubmitTemplateToVideoJob.md) <br>
- [DescribeTemplateToVideoJob reference](references/DescribeTemplateToVideoJob.md) <br>
- [Tencent Cloud SubmitTemplateToVideoJob documentation](https://cloud.tencent.com/document/product/1616/119001) <br>
- [Tencent Cloud DescribeTemplateToVideoJob documentation](https://cloud.tencent.com/document/product/1616/119002) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses with generated video URLs, job IDs, or error details; Markdown guidance for setup and command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials in environment variables and supports local image files or image URLs up to 10MB.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
