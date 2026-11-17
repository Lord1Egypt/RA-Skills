## Description:

Directly calls the Alibaba Cloud DashScope Qwen Wan 2.6 video generation model for text-to-video and image-to-video creation without an intermediate API proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchhao](https://clawhub.ai/user/wuchhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative automation agents use this skill to generate short videos from text prompts or reference image URLs through Alibaba Cloud DashScope. It supports parameterized video generation workflows that need direct API access and asynchronous result polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and the DashScope API key are sent to Alibaba Cloud DashScope for video generation.

Mitigation: Use only with provider approval, avoid confidential prompts or private image URLs unless allowed, and manage DASHSCOPE_API_KEY as a secret.

Risk: The artifact performs outbound API calls and long-running polling for generated video results.

Mitigation: Review generated commands before execution and add request timeouts or operational limits before heavy use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchhao/skills/qwen-wan-video)
- [DashScope API endpoint used by the artifact](https://dashscope.aliyuncs.com/api/v1)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; runtime functions return a video URL string.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and polls asynchronous DashScope tasks for up to 10 minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
