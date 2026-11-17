## Description:

该技能将学习问题路由给合适的技能，并仅在用户请求、获授权后汇总全景月报；它本身不讲题或发送提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

学生及陪同的家长或教师可用它将学习问题路由到合适的学习技能、避免重复处理，并在用户请求且数据获授权后汇总月报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reported a possible scope mismatch for consent-based profile writeback.

Mitigation: Before using the related integration, review which profile fields are requested and confirm the consent covers that scope.

Risk: Security analysis was partial because two references in SKILL.md did not resolve to bundled artifacts.

Mitigation: Resolve and inspect those references before relying on guidance that depends on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qizhitang/skills/xiaozhi-skill-coordinator)
- [Handover protocol schema](schemas/handover-protocol.schema.json)
- [One-week linkage example](references/one-week-linkage-record.md)
- [Crisis referral protocol](shared/crisis-referral-protocol.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [Chinese natural-language routing guidance, Markdown monthly reports, and JSON handover payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only task-relevant summaries when the user has authorized data sharing.]

## Skill Version(s):

2.12.7 (source: SKILL.md frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
