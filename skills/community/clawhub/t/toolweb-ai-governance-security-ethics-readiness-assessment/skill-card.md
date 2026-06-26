## Description: <br>
Assess organizational maturity across AI Governance, Security, and Ethics & Compliance domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, compliance, AI governance, and enterprise architecture teams use this skill to submit AI governance, security, and ethics readiness data to an external assessment API and receive maturity scores, findings, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assessment inputs may include sensitive governance, security, compliance, or organizational readiness details. <br>
Mitigation: Use pseudonymous session IDs, omit userId unless needed, and avoid submitting secrets, credentials, customer data, detailed vulnerabilities, or confidential control gaps unless the provider's privacy and retention practices are acceptable. <br>
Risk: The skill relies on an external ToolWeb service for assessment processing. <br>
Mitigation: Install and use only if sending selected readiness details to ToolWeb is appropriate for the organization and use case. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-ai-governance-security-ethics-readiness-assessment) <br>
- [ToolWeb API Route](https://api.toolweb.in/compliance/ai-governance-security-ethics) <br>
- [ToolWeb API Docs](https://api.toolweb.in:8172/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with JSON API request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an external ToolWeb assessment service and may return maturity scores, findings, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
