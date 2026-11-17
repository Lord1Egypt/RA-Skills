## Description:

腾讯云 TI-ONE 训推平台查询工具集，支持训练任务、在线服务、开发机、资源组、模型仓库、数据集、日志、事件等模块的查询操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Tencent Cloud TI-ONE training tasks, online services, notebooks, resource groups, model versions, datasets, logs, events, and console links through predefined read-only queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Tencent Cloud TI-ONE resource metadata, logs, events, and service details from the configured account.

Mitigation: Use credentials restricted to the required read-only Describe* actions and intended regions or resources.

Risk: The skill depends on tccli and jq being installed in the execution environment.

Mitigation: Install dependencies from controlled package sources, preferably in a virtual environment or similarly isolated runtime.

Risk: Returned logs and events may contain operational details that should not be broadly shared.

Mitigation: Run queries only for intended TI-ONE resources and avoid exposing secrets or sensitive log contents in responses.

## Reference(s):

- [TI-ONE tool parameter reference](references/cmd-reference.md)
- [TI-ONE console reference information](references/tione-guide.md)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/skiklvewddd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials, tccli, jq, and an intended TI-ONE region.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
