## Description: <br>
Based on computer vision, this skill analyzes videos or video URLs to detect coughing, phlegm, wheezing, and related respiratory symptom frequency for early health anomaly alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit respiratory monitoring videos, receive symptom counts, risk levels, health warnings, and medical suggestions, and list prior cloud-generated reports associated with the current session identity. The results are health-monitoring support and do not replace professional medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health videos, video URLs, and report history may be sent to remote services. <br>
Mitigation: Use only media appropriate for the service's privacy and retention practices, and avoid submitting private medical videos unless the service is trusted. <br>
Risk: The skill can silently create or reuse an account-linked identity and store tokens in a local workspace database. <br>
Mitigation: Run the skill in a separate workspace without shared secrets and review local token storage before deployment. <br>
Risk: Historical report listing can fetch account-linked health reports from cloud APIs. <br>
Mitigation: Require confirmation before listing report history and review returned report links before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-respiratory-symptom-recognition-analysis) <br>
- [Respiratory symptom recognition API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, Markdown tables, and structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links, symptom counts, risk scores, risk levels, warnings, and medical suggestions.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
