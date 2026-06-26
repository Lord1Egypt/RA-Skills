## Description: <br>
Assesses an organization's HIPAA compliance posture across administrative, physical, technical, privacy, and breach notification rule areas and produces a scored gap report with prioritized remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, security, and healthcare operations teams use this skill to evaluate HIPAA readiness for covered entities, business associates, or hybrid entities. It identifies control gaps, summarizes regulatory exposure, and prioritizes remediation actions for audit preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted organization and compliance details may be sensitive, especially when they describe PHI handling or security controls. <br>
Mitigation: Use the minimum detail needed, avoid patient-identifiable PHI unless approved, and confirm ToolWeb's privacy, retention, and HIPAA business-associate posture before submitting real organization data. <br>
Risk: HIPAA gap analysis output may be mistaken for legal advice or a final compliance determination. <br>
Mitigation: Treat the report as compliance planning guidance and have qualified legal, privacy, or compliance personnel review findings before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-hipaa-gap-analysis) <br>
- [HIPAA Gap Analysis API](https://portal.toolweb.in/apis/compliance/hipaa-gap-analysis) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb Portal](https://portal.toolweb.in) <br>
- [ToolWeb MCP Server](https://hub.toolweb.in) <br>
- [ToolWeb on RapidAPI](https://rapidapi.com/user/mkrishna477) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON report with compliance scores, gap lists, regulatory exposure summary, and prioritized remediation actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires organization profile details and HIPAA control status inputs; outputs should be reviewed as compliance planning guidance, not legal advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
