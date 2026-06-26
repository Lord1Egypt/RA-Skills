## Description: <br>
Recruiting supports hiring workflows with structured job descriptions, resume screening, interview preparation, candidate pipeline tracking, and draft communications while keeping candidate data local and reserving hiring decisions for humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting teams, hiring managers, and operators use this skill to organize human-led recruiting work, including job descriptions, structured screening criteria, interview preparation, candidate pipeline updates, and draft communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate ratings and outcome labels may steer hiring decisions despite the skill's stated boundary against automated decision-making. <br>
Mitigation: Use the skill only to organize human-led recruiting work, require a human reviewer for every hiring decision, and record final decisions outside the skill. <br>
Risk: Recruiting records may include protected characteristics or unnecessary personal data. <br>
Mitigation: Avoid storing protected characteristics or unnecessary personal data, and define retention and deletion practices before use. <br>
Risk: Screening summaries or draft communications may contain misleading, biased, or incomplete guidance. <br>
Mitigation: Review all screening output and communications before use and apply applicable employment-law and organizational compliance checks. <br>


## Reference(s): <br>
- [ClawHub Recruiting release page](https://clawhub.ai/AGIstack/recruiting-pro) <br>
- [Job Description Creation](references/job-descriptions.md) <br>
- [Resume Screening](references/resume-screening.md) <br>
- [Pipeline Tracking](references/pipeline-tracking.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and local JSON records, with shell commands for bundled data-operation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores recruiting records locally; human review is required for candidate assessments, communications, and hiring decisions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
