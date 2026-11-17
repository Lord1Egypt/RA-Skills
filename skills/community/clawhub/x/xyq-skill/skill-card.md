## Description:

使用小云雀生成和编辑图片、生成视频、超分、擦字幕及操作个人 Canvas 画布。新增图片模型动态查询、完整展示名称选模型及推理强度配置。需官方 CLI 1.0.33+，使用本人账号登录，生成任务按账号权益消耗积分；不包含短剧创作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ydtincle](https://clawhub.ai/user/ydtincle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route小云雀/XYQ requests into CLI-backed media generation, video processing, model discovery, credit checks, authentication, and personal Canvas operations. It helps agents prepare the right commands, query asynchronous results, and deliver generated image or video files when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open or reuse account login and relies on the user account's XYQ/Pippit permissions.

Mitigation: Confirm the intended account before authenticated operations and do not expose credentials or access keys in prompts, logs, or command arguments.

Risk: Generation and processing tasks may upload local media to the XYQ/Pippit service and consume account credits.

Mitigation: Only submit jobs after the user has provided the needed local files and authorized the credit-consuming operation.

Risk: Canvas operations can modify personal Canvas documents.

Mitigation: Query the target Canvas and IDs first, constrain edits to the requested scope, and verify the resulting Canvas state after writes.

Risk: The skill may install or cache the Pippit CLI to execute supported operations.

Mitigation: Use the bundled CLI check path, prefer validated cached or PATH binaries, and report installation or command availability failures instead of bypassing the CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ydtincle/skills/xyq-skill)
- [Publisher profile](https://clawhub.ai/user/ydtincle)
- [XYQ service endpoint](https://xyq.jianying.com)
- [Skill overview](artifact/SKILL.md)
- [Authentication](artifact/commands/auth.md)
- [Asynchronous delivery](artifact/workflows/async-delivery.md)
- [Canvas editing](artifact/workflows/canvas-edit.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files, Configuration]

**Output Format:** [Markdown guidance with CLI commands, JSON result handling, and delivered media file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or reuse a local Pippit CLI, upload local media, consume account credits, download generated assets, and modify personal Canvas documents when requested.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
