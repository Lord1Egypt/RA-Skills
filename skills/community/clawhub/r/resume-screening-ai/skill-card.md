## Description: <br>
帮助HR在实习生招聘中解析候选人PDF简历、对照岗位JD评估匹配度，并输出结构化筛选结论。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuxin-bit](https://clawhub.ai/user/qiuxin-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR and recruiting teams use this skill to compare intern resumes against a role JD, extract key candidate details, and produce a structured screening recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume screening can process personal candidate information. <br>
Mitigation: Handle resumes and extracted candidate details according to applicable privacy, retention, and access-control policies. <br>
Risk: Automated scoring can miss context, amplify biased criteria, or over-reject candidates based on incomplete resume evidence. <br>
Mitigation: Use the report as HR decision support, keep a human reviewer accountable for final decisions, and compare conclusions against job-relevant criteria. <br>
Risk: PDF conversion or resume parsing errors can lead to incorrect candidate facts. <br>
Mitigation: Review extracted fields against the original resume before relying on scores or recommendations. <br>


## Reference(s): <br>
- [简历筛选评估标准参考](references/screening-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown screening report with candidate details, scored evaluation dimensions, key conclusion, and recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a role JD and candidate resume content; PDF conversion may be needed before assessment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
