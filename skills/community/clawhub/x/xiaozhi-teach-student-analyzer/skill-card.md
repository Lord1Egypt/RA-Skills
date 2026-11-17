## Description:

将班级测验数据整理为学情画像、知识点薄弱项分析和可执行的教学调整建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

教师可用它分析班级或个体测验表现，定位知识点薄弱项，并据此制定分层教学调整。面向家长或学生的内容应由教师审定后再使用。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 学生成绩和个体诊断可能暴露敏感教育信息。

Mitigation: 优先使用学号或化名，公开报告使用聚合数据；生成家长内容前核对分享授权。

Risk: 启用前的统考试题、答案或评分标准可能受保密要求限制。

Mitigation: 仅分析已考完考试的逐题得分和题号到知识点的映射，不提交启用前的试题、答案或评分标准。

Risk: 有限的测评数据可能被误读为学生的稳定趋势或能力结论。

Mitigation: 至少有三次数据再作趋势判断；样本不足时标注证据不足，并由教师审核面向家长或学生的内容。

Risk: 安全审查为部分审查：有若干 SKILL.md 本地引用未解析，相关行为未获完整评估。

Mitigation: 依赖这些未解析引用所描述的行为前，先核对对应文件并完成完整审查。

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-student-analyzer)
- [学情分析框架](artifact/references/analysis-framework.md)
- [个体诊断卡模板](artifact/references/student-diagnosis-card-template.md)
- [班级学情报告模板](artifact/references/class-report-template.md)
- [危机例外处置](artifact/shared/crisis-exception.md)
- [危机转介流程](artifact/shared/crisis-referral-protocol.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, JSON]

**Output Format:** [Markdown 报告与表格，以及结构化班级记录]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [可包含班级画像、逐题统计、知识点热力图、个体诊断、分层和教学建议；数据不足时标注证据不足。]

## Skill Version(s):

2.12.7 (source: ClawHub release evidence; SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
