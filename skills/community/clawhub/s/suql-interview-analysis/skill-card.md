## Description:

第二阶段面试前简历匹配度分析，仅基于简历和岗位要求生成面试匹配度分析报告，并整合面试问答清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[suql82](https://clawhub.ai/user/suql82)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and interviewers use this skill to compare a candidate resume with a job description before an interview and generate a standardized matching report with interview focus questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate resumes may contain sensitive personal information.

Mitigation: Provide only the intended candidate folder and job description, and handle generated reports according to the organization's candidate-data policies.

Risk: A report may be incomplete or misleading if the resume or job description is missing.

Mitigation: Confirm with the user before proceeding when required materials are missing or the request is not clearly about resume matching.

Risk: Resume-to-job analysis can overstate facts if information outside the source documents is introduced.

Mitigation: Keep conclusions grounded in the provided resume and job description, and review the final report for unsupported additions or omissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suql82/skills/suql-interview-analysis)
- [Publisher profile](https://clawhub.ai/user/suql82)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [DOCX report with structured narrative sections, tables, and interview questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one `{姓名}-匹配度分析报告.docx` file based only on the candidate resume and job description.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
