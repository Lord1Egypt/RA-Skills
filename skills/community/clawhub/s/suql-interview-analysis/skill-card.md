## Description: <br>
第二阶段面试前简历匹配度分析 - 仅基于简历和岗位要求，生成面试匹配度分析报告（面试问答清单已整合） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suql82](https://clawhub.ai/user/suql82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR and recruiting teams use this skill before interviews to compare a candidate resume against a job description and generate a standardized matching analysis report with interview focus questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate resumes can contain personal data. <br>
Mitigation: Use only with appropriate authorization and limit input handling to the intended resume and job description materials. <br>
Risk: A generic matching-report request may be ambiguous about whether this HR workflow is intended. <br>
Mitigation: Confirm the user's intent before processing when the request does not clearly involve pre-interview resume-to-job matching. <br>
Risk: Missing resume or job description inputs can lead to incomplete or misleading analysis. <br>
Mitigation: Ask the user whether to continue and how to handle missing required documents before generating the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suql82/suql-interview-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured report content for a DOCX matching analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a six-chapter pre-interview matching report based on candidate resume and job description inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
