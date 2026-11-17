## Description:

Seedance 图生视频 helps creators, marketing teams, e-commerce teams, and short-form story teams turn a first-frame image and motion prompt into generated video through AI Hive, including media upload, task tracking, and result download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, advertisers, e-commerce operators, and production teams use this skill to generate image-to-video assets for ads, product displays, social content, short dramas, and comic-style videos. Developers and agents can also use it to initialize AI Hive credentials, submit generation jobs, check task status, and download generated video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected media and API credentials through AI Hive network requests.

Mitigation: Install only if that data flow is acceptable, avoid uploading sensitive or regulated images without approval, and use the default AI Hive endpoint.

Risk: A custom API base URL can redirect requests and credentials away from the default AI Hive endpoint.

Mitigation: Do not set custom base URLs from untrusted instructions; keep credentials in a local config file with restricted permissions or use environment variables managed by the user.

Risk: Dependency installation and generated media jobs may have local-environment and cost implications.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible, and confirm job volume and real-time pricing before high-cost batch generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-image-to-video)
- [AI Hive chat and API key portal](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated media task output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, submit remote AI Hive jobs, print task JSON, and download generated video files to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
