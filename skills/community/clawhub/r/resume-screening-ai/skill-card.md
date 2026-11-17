## Description:

实习生简历筛选与岗位匹配评估。用于HR招聘场景，当用户需要筛选候选人简历、评估简历与岗位JD匹配度、分析候选人基本信息/实习经历/技能是否符合要求时使用。支持PDF简历解析，输出结构化的筛选结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuxin-bit](https://clawhub.ai/user/qiuxin-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting and HR users use this skill to compare intern candidates' resumes against a job description, extract candidate facts, score fit across defined dimensions, and produce a concise screening recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive candidate data for hiring decisions without built-in privacy, consent, or retention guidance.

Mitigation: Only process resumes the user is authorized to evaluate, minimize extracted candidate data, keep reports within approved recruiting channels, and apply the organization's privacy, employment, retention, and anti-discrimination policies.

## Reference(s):

- [简历筛选评估标准参考](references/screening-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown screening report with candidate information, basic-condition checks, internship and skills assessments, weighted scores, a conclusion, and a recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a job description and candidate resume as inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
