## Description:

Seedance 2.5 首尾帧生视频 helps creators, marketing teams, e-commerce teams, and short-form production teams generate videos from first and last frame images through AI Hive, including material upload, task tracking, and result download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, e-commerce operators, and production teams use this skill to generate first-and-last-frame image-to-video assets for ads, product displays, social posts, short dramas, and comic-style videos through AI Hive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be sent to a configurable endpoint.

Mitigation: Use only trusted AI Hive base URLs, avoid untrusted --base-url or AI_HIVE_BASE_URL values, and rotate the API key if it may have been sent to the wrong endpoint.

Risk: Downloaded results may be written using untrusted remote metadata.

Mitigation: Keep the output directory away from sensitive configuration files and review downloaded files before reuse.

Risk: The skill can initiate spend-capable video-generation tasks.

Mitigation: Confirm task volume and live pricing before batch use, and treat the API key as spend-capable.

Risk: Runtime dependencies and local configuration affect execution.

Mitigation: Review before installing and consider an isolated virtual environment with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-5-first-last-frame-to-video)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands, configuration values, task identifiers, status text, and downloaded video files when enabled.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials and may submit paid video-generation tasks; generated media is saved to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
