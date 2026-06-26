## Description: <br>
AI-powered voice mock interview platform that analyzes job descriptions and conducts adaptive interviews with real-time feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, recruitment platforms, training teams, and educational institutions use this skill to integrate Interviewly's job description analysis, adaptive mock interview flow, response feedback, and report generation into interview preparation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interview answers, job descriptions, and generated reports are sensitive content sent to Interviewly/toolweb and Claude for evaluation. <br>
Mitigation: Avoid submitting secrets, confidential employer information, or highly sensitive personal details, and use the service only with appropriate consent. <br>
Risk: Session IDs and report URLs may expose completed interview artifacts because the evidence does not describe retention, deletion, authentication, or link expiration. <br>
Mitigation: Protect session IDs and report URLs, share them only with intended recipients, and confirm retention or deletion controls before production use. <br>


## Reference(s): <br>
- [Interviewly API Docs](https://api.toolweb.in:8173/docs) <br>
- [Interviewly Kong Route](https://api.toolweb.in/tools/interviewly) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents a remote API workflow that returns JSON interview state, feedback, scores, and PDF report download URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openapi.json info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
