## Description:

Generates videos with Alibaba Cloud Model Studio Wan text-to-video models by submitting asynchronous jobs, polling status, and downloading MP4 outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouweico](https://clawhub.ai/user/zhouweico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Wan text-to-video jobs from prompts, resume polling with an existing task ID, and save generated video files locally after reviewing preflight cost and model settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom base URL or untrusted config can receive the DashScope API key.

Mitigation: Use a trusted config.json and environment, keep DASHSCOPE_BASE_URL unset unless a vetted DashScope endpoint is required, and review the resolved endpoint before running.

Risk: Storing the API key in config.json can expose credentials through local file access or accidental sharing.

Mitigation: Prefer DASHSCOPE_API_KEY in the environment and avoid committing or distributing config.json files containing secrets.

Risk: Successful runs write generated MP4 files to outputs/ or the configured output directory.

Mitigation: Choose an appropriate output directory and review generated media before sharing or reusing it.

## Reference(s):

- [Wan Video Generation API Notes](references/api.md)
- [Alibaba Cloud Model Studio Text-to-Video API Reference](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)
- [Alibaba Cloud Model Studio Text-to-Video Guide](https://help.aliyun.com/zh/model-studio/text-to-video-guide)
- [Alibaba Cloud Model Studio Video Generation](https://help.aliyun.com/zh/model-studio/use-video-generation)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [CLI text output, JSON request previews, and local MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs write MP4 files under outputs/ or the configured output directory; --dry-run prints the resolved request, selected model settings, and estimated China mainland cost without submitting a task.]

## Skill Version(s):

0.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
