## Description:

批量编排 WBFlow 短片生产流程，为每个条目创建独立工作目录、维护状态并汇总成品，支持断点续跑和定时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

短片制作人员和自动化工作流开发者可用此 skill 按清单批量调度 WBFlow 流程，为每条内容独立运行、续跑并汇总成品。需要同时安装 wbflow-pipeline 和八个阶段 skill。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe file handling can overwrite unrelated files or include unintended media.

Mitigation: Use trusted batch configurations and manifests.

Risk: Montage generation has temporary-file protection, filename escaping, and directory containment concerns.

Mitigation: Address these concerns before enabling montage.

Risk: Scheduled production depends on companion skills being suitable for the intended workflow.

Mitigation: Review the companion skills before enabling scheduled production.

## Reference(s):

- [WBFlow 批量工厂 on ClawHub](https://clawhub.ai/junci003/skills/wbflow-batch)

## Skill Output:

**Output Type(s):** [Video files, JSON configuration and manifests, Files]

**Output Format:** [MP4 video files and JSON batch configuration, seeds, and manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a separate work directory per batch item; companion WBFlow skills are required.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
