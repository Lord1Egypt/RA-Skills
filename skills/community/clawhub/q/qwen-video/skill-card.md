## Description:

Generate videos using Alibaba Cloud DashScope Wan text-to-video APIs, including async submission, status polling, and local MP4 download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[547895019](https://clawhub.ai/user/547895019)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to request short Wan text-to-video generations through DashScope, monitor the async task, and save the resulting MP4 locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell networking could expose valuable DashScope credentials or accept unexpected TLS endpoints.

Mitigation: Remove curl -k, require normal TLS verification, and use only non-sensitive prompts and audio URLs until the scripts are reviewed and hardened.

Risk: Crafted prompt, audio URL, or option values could break JSON construction or influence shell execution.

Mitigation: Validate arguments and build request JSON with a structured encoder before using valuable API credentials.

Risk: Returned media URLs may not be constrained to expected HTTPS hosts before download.

Mitigation: Allow downloads only from expected HTTPS result hosts and reject unexpected schemes or domains.

## Reference(s):

- [DashScope Wan t2v API notes](references/api.md)
- [DashScope video synthesis endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis)
- [ClawHub skill page](https://clawhub.ai/547895019/skills/qwen-video)
- [ClawHub publisher profile](https://clawhub.ai/user/547895019)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and status/output lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task identifiers, video URLs, and local MP4 file paths when generation succeeds.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
