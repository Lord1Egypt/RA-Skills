## Description:

为初高中生物教师生成围绕观察、实验和证据推理组织的教案草稿、探究活动方案与递进式提问链。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT

## Use Case:

面向中国大陆初中和高中生物教师，用于规划单元与课时、设计探究和学生实验、组织复习或讲评课，并形成可由教师审定的教学草稿。

### Deployment Geography for Use:

中国大陆（中文 K12 教育场景；其他地区使用前需本地化课程口径、法规与求助渠道）

## Known Risks and Mitigations:

Risk: 安全证据不完整：扫描结论为 benign、中等置信度，且 Skillspector 覆盖部分缺失。

Mitigation: 按扫描 guidance 评估未匹配的本地引用带来的不确定性，并在安装前复核。

Risk: 实验活动可能涉及器材、试剂或生物材料安全。

Mitigation: 按技能所引用的实验安全分档设计；高档内容由教师演示或改用视频，中档活动由教师全程在场，不安排在家培养微生物或采血。

Risk: 学生个人信息、健康信息和未启用的考试材料属于敏感内容。

Mitigation: 避免输入个人信息和未启用试题；教案记录使用化名或座号，分批考试须等全部批次结束后再讲评。

Risk: 课堂健康内容可能被误作针对学生的诊断或治疗建议。

Mitigation: 依教材组织内容，不根据学生健康状况举例，不提供诊断、用药或治疗建议，并由教师审定面向学生或家长的材料。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-biology-lesson-planner)
- [Publisher profile](https://clawhub.ai/user/qizhitang)
- [Biology curriculum map](artifact/references/biology-curriculum-map.md)
- [Required high-school biology units](artifact/references/biology-hs-units-required.md)
- [Elective high-school biology units](artifact/references/biology-hs-units-elective.md)
- [Laboratory safety guidance](artifact/shared/lab-safety.md)
- [Crisis exception guidance](artifact/shared/crisis-exception.md)
- [AI-generated item review protocol](artifact/shared/ai-item-check.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown lesson-plan drafts, experiment outlines, and question sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts for teacher review; generated learning materials and questions require the stated checks before classroom or resource-library use.]

## Skill Version(s):

2.12.7 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
