## Description: <br>
AI简历评分助手。根据用户上传的简历（含Markdown文本或文件），按照AI领域满分/及格线两份参考简历为基准，计算简历能力值（满分100分）。若简历非AI领域，则进行跨行业等价换算，评估该简历在其所属行业的能力水平。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclecheng-li](https://clawhub.ai/user/unclecheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate pasted resume text or a selected resume file against a weighted resume scoring rubric, including AI-domain scoring and cross-industry equivalent scoring for non-AI resumes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume inputs may contain sensitive personal information. <br>
Mitigation: Use only pasted text or an explicitly selected resume file, and avoid pointing the skill at unrelated local files. <br>
Risk: Running the Python helper directly can read a local file path and write resume-derived report data to a fixed desktop path. <br>
Mitigation: Run the helper only in a controlled workspace and review or redirect the output path before processing sensitive resumes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unclecheng-li/unclecheng-ai-resume-judge) <br>
- [Resume scoring benchmark](references/scoring_benchmark.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured Markdown scoring report with optional JSON report data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include a numeric score, dimension breakdown, detected industry, cross-industry equivalent score when applicable, detailed comments, and top improvement suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
