## Description:

通过平台 API 获取数字人与音色、训练资源并合成口播视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuhongfeii2](https://clawhub.ai/user/xuhongfeii2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list available digital humans, voices, and fonts, train custom digital-human or voice assets, and synthesize talking-head videos through the configured platform API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says this version may send API tokens, scripts, voice recordings, videos, images, and task results to the easyclaw.bar platform.

Mitigation: Install only for accounts and networks where that data sharing is acceptable, and review platform access before use.

Risk: The security guidance notes that current artifacts default to HTTP, which may expose credentials and media in transit.

Mitigation: Prefer HTTPS or a trusted network path before using production credentials or sensitive media.

Risk: The security guidance warns against enabling the async watcher while credentials may be written into cron prompts or command-line arguments.

Mitigation: Avoid the async watcher until credential handling is reviewed, and rotate tokens previously used with this version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuhongfeii2/skills/shuziren-koubo-shengcheng)
- [Publisher profile](https://clawhub.ai/user/xuhongfeii2)
- [Platform API Reference](references/platform-api.md)
- [Setup Guide](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON script results and media links when tasks return images or videos]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task identifiers, watcher status, direct video URLs, image previews, and setup instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
