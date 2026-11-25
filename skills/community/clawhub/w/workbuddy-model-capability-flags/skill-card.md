## Description:

排查并修复 WorkBuddy 自定义模型的读图、工具调用和推理能力标记，并探测新模型能力后生成配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using WorkBuddy can diagnose incorrect capability flags for custom models, verify image, tool-call, and reasoning support, and update model configuration for a new compatible endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports possible broad cleanup of temporary backups and configuration writes that could discard unrelated settings.

Mitigation: Review the exact files and fields the probe may change, make a backup, and inspect the configuration diff before applying results.

Risk: Image capability checks send a test image to the configured model endpoint.

Mitigation: Use a non-sensitive test image unless you have reviewed where that endpoint sends and stores requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/workbuddy-model-capability-flags)

## Skill Output:

**Output Type(s):** [Guidance, Python code, Shell commands, JSON configuration]

**Output Format:** [Markdown guidance, Python code, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The probe can optionally write capability results to the model configuration file.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
