## Description: <br>
Generate interview question bank and answer strategy from JD and company intel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghong5233](https://clawhub.ai/user/wanghong5233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to prepare concise, actionable interview materials from a job description, company details, or a recent job record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job descriptions, company details, and interview-preparation inputs may contain sensitive hiring or personal information. <br>
Mitigation: Use the skill only with a trusted local job-analysis service and avoid submitting confidential material unless its storage and logging behavior is acceptable. <br>
Risk: A local service listening on the expected endpoint may be misconfigured or unexpected. <br>
Mitigation: Confirm what process is bound to http://127.0.0.1:8010/api/interview/prep before sending job data. <br>
Risk: Interview guidance can be overstated as predictive. <br>
Mitigation: Present recommendations as likely focus areas with confidence, and do not claim certainty about interview outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanghong5233/wanghong5233-offerpilot-interview-prep) <br>
- [Publisher profile](https://clawhub.ai/user/wanghong5233) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise interview summaries, likely focus areas, storylines, question banks, answer tips, and optional curl command templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses either a job_id or company, role title, and job description text; presents interview focus as likely guidance rather than certainty.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
