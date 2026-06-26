## Description: <br>
Evaluate SOC 2 Type I or Type II readiness across the five Trust Services Criteria and return a readiness score, gap analysis, audit recommendation, remediation roadmap, and evidence checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, compliance, and audit-readiness teams use this skill to assess current SOC 2 control posture, identify gaps, and prioritize remediation before engaging in a Type I or Type II audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SOC 2 posture details are sent to ToolWeb's third-party API. <br>
Mitigation: Confirm ToolWeb is the intended provider, review its privacy and retention terms, and avoid submitting secrets, customer data, detailed network diagrams, or internal evidence files unless sharing them with that service is acceptable. <br>
Risk: API credentials used with the service could expose unnecessary access if reused or leaked. <br>
Mitigation: Use a dedicated API key for this skill and rotate or revoke it according to your organization's credential handling policy. <br>
Risk: Readiness scores, remediation timelines, and evidence requests may not fully match a specific audit scope. <br>
Mitigation: Treat the output as planning guidance and validate control mappings, evidence, and audit scope with compliance owners or an auditor before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-soc2-readiness) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb API Portal](https://portal.toolweb.in) <br>
- [ToolWeb MCP Server](https://hub.toolweb.in) <br>
- [RapidAPI ToolWeb Profile](https://rapidapi.com/user/mkrishna477) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON assessment with readiness scores, gap analysis, audit type advice, remediation roadmap, timeline, and evidence checklist.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires company profile, cloud service, and control posture inputs; authentication is required for the third-party service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
