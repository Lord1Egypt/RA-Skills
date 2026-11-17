## Description:

帮助初中和高中数学教师根据作业与测评数据归类错因、关联知识点，并形成班级和个体画像及教学建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

面向初中和高中数学教师，用于从作业或测评作答数据中发现班级共性与个体错误模式、定位知识薄弱点，并拟定教学干预建议。分析结果及档案更新由教师审核，技能不代替教师阅卷或作教学决定。

### Deployment Geography for Use:

中国（面向中国初高中数学课程与学校教学场景）

## Known Risks and Mitigations:

Risk: ClawScan 的结论为 benign、置信度 medium；扫描覆盖不完整，且报告了一项与 lesson-planning 范围重叠的 concern。

Mitigation: 安装前检查该技能的职责范围，并确认文档中提到的相关指导材料可用。

Risk: 作答记录可能含有学生个人信息；统考启用前试题及答案也可能属于敏感内容。

Mitigation: 使用化名或编号，避免输入真实姓名与未启用考试材料，并按技能文档在考试全部结束后再分析相关错题。

Risk: AI 生成的针对性练习可能存在数学错误。

Mitigation: 按技能文档先自检并标注为 AI 生成；教师验算前不要将题目放入作业或试卷。

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-math-error-analyzer)
- [Error classification rubric](artifact/references/error-classification-rubric.md)
- [Knowledge map template](artifact/references/knowledge-map-template.md)
- [Intervention design](artifact/references/intervention-design.md)
- [Class teaching workspace schema](artifact/shared/class-teaching-workspace.schema.json)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, JSON]

**Output Format:** [中文分析报告与教学建议，通常以 Markdown 表格或结构化条目呈现]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [可包含班级或个体错因画像、知识点关联和待教师确认的工作区更新；抽样数据需标明样本量，AI 生成的练习题需教师验算。]

## Skill Version(s):

2.12.7 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
