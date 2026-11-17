## Description:

Xplai Video helps agents submit text or image-guided requests to Xplai's external service to generate explainer videos in English or Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyxu](https://clawhub.ai/user/yuanyxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate explainer or tutorial videos from prompts, optional image URLs, math problems, news summaries, code explanations, or language-learning material. It submits jobs to Xplai and checks status until a generated video URL or failure is returned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video descriptions, optional image URLs, and video IDs are sent to Xplai's external API.

Mitigation: Avoid confidential business material, private images, secrets, and internal URLs in prompts or image inputs.

Risk: Debug mode can print request and response details that may contain sensitive prompts or service responses.

Mitigation: Use debug mode only in controlled troubleshooting contexts and avoid it for sensitive requests.

Risk: The skill depends on an external video-generation service and asynchronous status polling.

Mitigation: Check returned status values before sharing outputs and handle failed or queued jobs as incomplete results.

## Reference(s):

- [Xplai official website](https://www.xplai.ai/)
- [ClawHub skill page](https://clawhub.ai/yuanyxu/skills/xplai-video)
- [ClawHub publisher profile](https://clawhub.ai/user/yuanyxu)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status messages with generated video IDs, queue status, and video URLs when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a generated video URL and Xplai web page URL after successful status polling.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
