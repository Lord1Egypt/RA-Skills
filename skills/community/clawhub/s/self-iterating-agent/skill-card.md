## Description:

具备持续自主进化、长期记忆、全流程自主执行能力的高级自迭代智能体，支持长周期复杂任务的拆解规划、技能匹配、执行落地、排障修复、复盘优化和能力进化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangruoqing86-stack](https://clawhub.ai/user/yangruoqing86-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this agent skill to plan and run long-duration automation workflows that require task decomposition, skill matching, progress tracking, retry handling, review, and cross-agent coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended command execution and automatic installation can change the environment without timely review.

Mitigation: Run the skill in a constrained environment, require per-task approval, and disable or tightly restrict exec-plus and automatic installs.

Risk: Scheduled autonomous activity can continue longer than intended.

Mitigation: Set explicit schedule expiration, revocation controls, and regular operator review for any recurring task.

Risk: Long-term memory can retain sensitive task history or secrets.

Mitigation: Do not store secrets or sensitive history in long-term memory, and review memory retention settings before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangruoqing86-stack/skills/self-iterating-agent)
- [Publisher profile](https://clawhub.ai/user/yangruoqing86-stack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with plans, status updates, commands, configuration changes, and delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate autonomous execution steps, scheduled follow-ups, retries, skill installation requests, and long-term memory updates when permitted by the runtime.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
