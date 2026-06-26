## Description: <br>
Analyzes bathroom doorway or privacy-filtered bathroom video to track elderly toilet entry and exit events, calculate continuous occupancy time, and alert when the stay exceeds a configured threshold, defaulting to 30 minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregiving teams, nursing-home operators, and home-safety platform developers use this skill to monitor privacy-filtered bathroom occupancy videos for prolonged toilet stays and to produce alerts or history reports for human follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive bathroom-door or privacy-filtered bathroom video and identity data through a remote API. <br>
Mitigation: Use the skill only with consent from the monitored person or caregiver, prefer doorway footage or blurred silhouette-only footage, and avoid uploading unblurred interior bathroom video. <br>
Risk: Remote analysis and history lookup require an open-id that can be associated with report records. <br>
Mitigation: Use a dedicated open-id where possible and review or clear local workspace data if token or identifier persistence is a concern. <br>
Risk: Alerts are based on occupancy timing and are not medical diagnoses or emergency instructions. <br>
Mitigation: Treat alerts as prompts for human verification and route urgent cases to caregivers or local emergency procedures. <br>


## Reference(s): <br>
- [API Documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries or tables, JSON analysis results, and command-line invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis may include occupancy duration, alert level, alert message, session history, suggested contacts, and optional report links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
