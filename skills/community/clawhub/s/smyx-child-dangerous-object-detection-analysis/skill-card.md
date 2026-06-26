## Description: <br>
Analyzes child activity footage or URLs for contact with dangerous objects or electrical sockets and returns structured warning results with report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, childcare staff, and smart-camera developers use the skill to submit child activity images, videos, or URLs for dangerous-object and socket-contact detection. The skill returns structured alerts, report links, and cloud-backed historical report listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child-monitoring images, videos, URLs, and generated reports are sent to the LifeEmergence cloud service. <br>
Mitigation: Install only where the user has appropriate guardian consent and has reviewed the service's data handling, retention, and access controls. <br>
Risk: The skill silently creates or reuses a local identity and can store service tokens in a local SQLite database. <br>
Mitigation: Use isolated workspaces, protect local data files, and avoid shared machines unless identity files and token storage are separately managed. <br>
Risk: Historical report queries retrieve cloud-stored report data associated with the resolved identity. <br>
Mitigation: Confirm the runtime identity is authorized for the requested reports and keep report listings out of unauthorized logs or transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-child-dangerous-object-detection-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files] <br>
**Output Format:** [Structured text, Markdown tables or JSON with optional report export links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the returned analysis to a user-specified output file and may include cloud report image links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
