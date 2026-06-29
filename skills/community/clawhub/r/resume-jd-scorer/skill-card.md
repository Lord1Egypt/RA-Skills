## Description: <br>
简历-JD匹配度5维度评分技能。输入简历文本和目标JD，自动提取关键词、交叉匹配、5维评分，并生成交互式HTML报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers, recruiters, and career advisors use this skill to compare resume content against a target job description, score fit across five dimensions, and identify high-impact resume improvements. It is intended for structured resume diagnosis, not for inventing new candidate facts or rewriting the original resume file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume and job description text can contain personal or sensitive information. <br>
Mitigation: Provide only the resume and JD content you are comfortable letting the agent read, and provide sensitive JD text directly instead of asking the skill to search externally. <br>
Risk: The skill writes local scoring reports that may be stored in a shared or unintended location. <br>
Mitigation: Choose an output directory appropriate for the sensitivity of the resume and review generated files before sharing them. <br>
Risk: Resume scoring and recommendations may be incomplete or misleading if inputs are missing, stale, or not representative of the target role. <br>
Mitigation: Review the generated score, matched keywords, deductions, and TOP3 suggestions before using the report for application or hiring decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/resume-jd-scorer) <br>
- [Scoring rubric](references/scoring-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [Text guidance plus local JSON, HTML, and Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates resume-output/<version>/jd-match-report.html and jd-match-report.md when run with provided resume and JD content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
