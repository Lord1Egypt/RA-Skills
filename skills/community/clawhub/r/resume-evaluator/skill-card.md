## Description: <br>
根据对话输入的 JD 或通用标准，批量评估简历并输出带颜色评级的表格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengchchen](https://clawhub.ai/user/zhengchchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hiring teams and recruiters use this skill to compare resumes in a chosen folder against a job description or default senior frontend engineering criteria. It produces ranked candidate recommendations with scores, ratings, and concise fit notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate resumes can contain personal information and sensitive employment history. <br>
Mitigation: Use a dedicated folder containing only resumes intended for evaluation, and confirm permission before processing or sharing candidate information. <br>
Risk: Automated resume scoring may miss context or overstate fit when used as the only hiring signal. <br>
Mitigation: Treat the generated table as a review aid and have qualified reviewers verify resume facts, scoring criteria, and recommendations before making decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhengchchen/resume-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, guidance] <br>
**Output Format:** [Markdown table with candidate scores, color-coded ratings, extracted resume attributes, technology stack, and concise fit evaluation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sorts candidates by rating priority and score; uses user-provided JD criteria when available.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
