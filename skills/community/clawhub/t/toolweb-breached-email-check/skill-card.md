## Description: <br>
Checks whether an email address appears in known data breaches and returns breach history, exposed data types, severity, paste exposure, and remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, developers, and administrators use this skill to check authorized email addresses for breach exposure during onboarding, employee audits, threat assessments, password reset decisions, and security awareness workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted email addresses and returned breach intelligence are sensitive security data. <br>
Mitigation: Use the skill only for email addresses you own or are authorized to check, and restrict access to generated results. <br>
Risk: The skill depends on ToolWeb handling submitted emails and breach lookup results. <br>
Mitigation: Install only if you trust ToolWeb for this data flow, and use a scoped, revocable API key where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-breached-email-check) <br>
- [ToolWeb breach email check API](https://portal.toolweb.in/apis/security/breached-email-check) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb portal](https://portal.toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Guidance] <br>
**Output Format:** [JSON response with breach status, breach details, severity, paste exposure, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may contain sensitive breach intelligence and should be protected accordingly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
