## Description: <br>
AI-powered customer success knowledge management for searching account health data, onboarding records, renewal tracking, and support escalation documentation with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success teams and account leaders use this skill to search customer health, onboarding, renewal, stakeholder, and support-escalation knowledge. It helps prepare portfolio reviews, account handoffs, churn-risk assessments, renewal checks, and targeted knowledge updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad organizational customer-success context can include sensitive account, financial, relationship, renewal, and escalation data. <br>
Mitigation: Install only for authorized organizations and confirm authorization, audit logging, redaction, and approval controls before enabling bulk exports. <br>
Risk: A configured API key is used with a remote MCP service. <br>
Mitigation: Use a scoped, revocable API key, prefer HTTPS-only endpoints, and rotate or revoke the key if access changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RooJenkins/uplo-customer-success) <br>
- [Publisher Profile](https://clawhub.ai/user/RooJenkins) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO Schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline tool commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retrieve and export organizational customer-success context through the configured UPLO MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
