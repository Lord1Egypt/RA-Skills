## Description: <br>
Screens resumes for authenticity risk, packaging risk, and role fit, producing an evidence-based risk report and ATS-oriented JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donotwannatry](https://clawhub.ai/user/donotwannatry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR staff and technical interviewers use this skill to batch-screen candidate resumes, OCR text, or public context for authenticity risk, inflated claims, timeline issues, role fit, and follow-up interview questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fixed Chinese-language behavior may limit usability for teams that need another output language. <br>
Mitigation: Install and use the skill only when Chinese-language reporting fits the workflow. <br>
Risk: Resume text is untrusted input and may contain prompt-injection attempts or non-resume content. <br>
Mitigation: The skill directs the agent to block prompt override attempts, reject forced-evaluation instructions, and return INVALID_INPUT for non-resume text. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown report followed by a JSON code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes candidate/contact extraction, risk flags, role classification, usability state, and background-check focus arrays.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
