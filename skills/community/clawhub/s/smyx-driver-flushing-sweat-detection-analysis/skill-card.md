## Description: <br>
Analyzes in-cabin DMS camera video to detect driver facial flushing and abnormal sweating, then returns visual health-risk reminders and recommended rest, alert, upload, or event-record actions without making medical diagnoses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, fleet operators, and DMS integrators use this skill to analyze driver-facing RGB video for visual signs of facial flushing or sweating and to produce reminder, fleet-upload, or event-record outputs. It is intended as an auxiliary driver-awareness signal, not as a medical diagnostic system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive driver video and identifiers may be uploaded to remote services without clear consent, retention, fleet-sharing, or backend assurance. <br>
Mitigation: Verify the publisher and backend service before use, and require written controls for driver consent, video upload and retention, fleet sharing, encryption, and URL validation. <br>
Risk: Historical report access and account or token handling may expose driver health-event records if authorization and storage controls are weak. <br>
Mitigation: Confirm report-query authorization, least-privilege access, auditability, and secure token storage before enabling history lookup. <br>
Risk: The skill can be mistaken for medical diagnosis even though its outputs are visual anomaly reminders. <br>
Mitigation: Present outputs as auxiliary visual alerts only, avoid clinical conclusions, and direct users to professional medical evaluation when health symptoms are present. <br>
Risk: Dependency and code-domain mismatches may create installation or operational risk. <br>
Mitigation: Replace the `yaml` dependency with the intended package and test the service integration before deployment. <br>


## Reference(s): <br>
- [Driver Facial Flushing / Sweat Abnormality Detection API Documentation](references/api_doc.md) <br>
- [ClawHub Skill Release Page](https://clawhub.ai/smyx-sunjinhui/smyx-driver-flushing-sweat-detection-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/smyx-sunjinhui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON analysis results or Markdown report tables with shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a driver video URL or local video file and a valid open-id/API credential before analysis or history lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
