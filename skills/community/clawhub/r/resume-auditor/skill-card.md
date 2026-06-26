## Description: <br>
Audits programmer resumes for timeline logic issues, weakly quantified project claims, privacy-sensitive contact details, and formatting improvements, then can generate a polished Word resume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[putao2882-ui](https://clawhub.ai/user/putao2882-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers, resume reviewers, and agents assisting candidates use this skill to check resume text for common logic flaws, missing quantification, and privacy exposure before producing a recruiter-ready resume document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume text can contain personal contact details and employment history. <br>
Mitigation: Use the anonymized mode before sharing generated resumes publicly or with untrusted recipients. <br>
Risk: Unpinned Python dependencies can change behavior across installations. <br>
Mitigation: Review or pin the Python dependencies before using the skill in production or shared environments. <br>
Risk: Automated resume scoring and logic checks may miss context or flag valid chronology as a flaw. <br>
Mitigation: Have the candidate or reviewer confirm the audit findings before editing or submitting the resume. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/putao2882-ui/resume-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, code, guidance] <br>
**Output Format:** [Structured resume audit findings and generated DOCX resume file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preserve or anonymize phone and email details depending on the selected privacy mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
