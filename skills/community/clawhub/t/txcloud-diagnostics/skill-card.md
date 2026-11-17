## Description:

用于腾讯云云产品异常诊断。当用户反馈腾讯云相关的任何异常、产品/实例不可用等情况时，根据反馈的实例和异常信息，自动拉取监控等数据进行分析诊断，输出原因和建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[crueluncle](https://clawhub.ai/user/crueluncle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to diagnose Tencent Cloud product incidents by collecting instance details, monitoring metrics, and time-bounded failure context, then producing a concise conclusion and recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent Cloud login handling and temporary authorization files may expose sensitive credentials or auth codes.

Mitigation: Use least-privilege Tencent Cloud credentials, treat auth codes and /tmp log files as sensitive, and clean up daemon and temporary auth files after use.

Risk: The skill can invoke Tencent Cloud TAT remote shell execution on cloud instances.

Mitigation: Do not allow TAT commands unless each command is explicitly approved and understood before execution.

Risk: Remote shell execution lacks strong technical limits and clear per-action user approval in the submitted evidence.

Mitigation: Review the skill before installation and require human approval for any cloud action that changes execution state or accesses sensitive resources.

## Reference(s):

- [Tencent Cloud product documentation](https://cloud.tencent.com/document/product)
- [ClawHub skill page](https://clawhub.ai/crueluncle/skills/txcloud-diagnostics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic report with command snippets and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary JSON reports and Tencent Cloud authorization files under /tmp during execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
