## Description:

连锁门店巡店管理全流程助手，覆盖巡店计划制定、巡店执行评分、营销方案生成和数据分析报告，支持10维加权评分、交互式HTML报告、多门店对比和整改追踪闭环。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Store operations teams and retail supervisors use this skill to plan inspections, score store execution, generate marketing improvement actions, and analyze inspection history across locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can run injected script from inspection data.

Mitigation: Use only trusted inspection data and avoid opening generated HTML reports built from untrusted store names or issue text.

Risk: Generated reports load Chart.js from a remote CDN.

Mitigation: Prefer a fixed version that bundles or pins Chart.js locally before production use.

Risk: The release security verdict is suspicious.

Mitigation: Review this skill before installing it in a production or sensitive business workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/store-inspection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; script workflows generate JSON data files and interactive HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local data and output files for inspection plans, scoring results, marketing plans, demo data, and HTML analysis reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
