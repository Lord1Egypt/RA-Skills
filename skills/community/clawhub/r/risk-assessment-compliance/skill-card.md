## Description: <br>
Performs comprehensive security checks and compliance risk assessments on websites and applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, compliance officers, DevOps engineers, penetration testers, and application security engineers use this skill to assess websites or applications for vulnerabilities, compliance status, risk level, and remediation priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted target URLs are sent to the external ToolWeb/MKKPro service. <br>
Mitigation: Use the skill only for websites or applications you own or are explicitly authorized to test, and avoid submitting internal, staging, credential-bearing, or sensitive URLs unless your organization has approved that sharing. <br>
Risk: Automated vulnerability and compliance results may be incomplete or unsuitable as sole audit evidence. <br>
Mitigation: Have security or compliance staff review findings, validate remediation steps, and confirm results before relying on them for audit or certification decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/risk-assessment-compliance) <br>
- [API Documentation](https://api.mkkpro.com:8014/docs) <br>
- [Risk Assessment API Route](https://api.mkkpro.com/compliance/risk-assessment) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON security and compliance assessment response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target URL and sends it to the external provider for assessment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
