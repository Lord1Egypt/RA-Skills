## Description: <br>
Analyzes respiratory symptom media with cloud computer-vision services to detect coughing, sputum-clearing, and wheezing frequency, then returns structured monitoring results, health alerts, care suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-support agents use this skill to submit respiratory monitoring videos or video URLs, receive symptom frequency counts and risk signals, and retrieve prior cloud-generated reports. Results are for health monitoring support and do not replace professional medical diagnosis or emergency care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive respiratory videos or provided video URLs may be sent to a cloud service for analysis. <br>
Mitigation: Use only with informed user consent and after confirming appropriate privacy, retention, deletion, and account-scoping controls for health media. <br>
Risk: The skill may create or reuse an internal identity and persist API tokens in a local SQLite database. <br>
Mitigation: Restrict workspace access, review token storage and rotation practices, and clear local stored identity data when it is no longer needed. <br>
Risk: Health alerts and care suggestions may be mistaken for medical diagnosis. <br>
Mitigation: Present outputs as monitoring support only, and direct users to professional medical care for diagnosis, treatment decisions, severe symptoms, or emergencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-respiratory-symptom-recognition-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Respiratory analysis API documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON report text with structured symptom counts, risk level, health warnings, care suggestions, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save output to a requested file and can list prior cloud-generated reports as structured text.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
