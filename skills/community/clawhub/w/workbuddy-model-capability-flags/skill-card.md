## Description:

帮助排查 WorkBuddy 自定义模型的读图、工具调用和推理能力位，探测兼容端点并指导修正配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy 用户和开发者可检测自定义模型是否支持图片、工具调用和推理档位，并在核对结果后修正或新增本地模型配置。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Probing sends requests to configured model endpoints and can transmit a supplied private image.

Mitigation: Use trusted endpoints and avoid supplying private images unless you trust the endpoint; probe without changes first.

Risk: Applying probe results or adding a model changes local capability settings.

Mitigation: Review the reported changes before using --apply or --add, retain the configuration backup, and restart WorkBuddy to load the changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/workbuddy-model-capability-flags)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only probing by default; configuration changes require explicit application.]

## Skill Version(s):

1.0.0 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
