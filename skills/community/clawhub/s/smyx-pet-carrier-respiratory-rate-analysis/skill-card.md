## Description: <br>
Analyzes local pet-carrier videos or video URLs through server-side APIs to estimate resting respiratory rate, compare it with safety thresholds, flag abnormal patterns, and return non-diagnostic transport-risk alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-transport operators can use this skill to analyze airline-carrier pet videos for respiratory-rate monitoring during transport. It returns objective breathing-rate observations, threshold alerts, and historical report links without providing disease diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos or video URLs may be sent to a remote service and linked to an open-id, username, or phone number. <br>
Mitigation: Use non-sensitive identifiers where possible, avoid real phone numbers unless required, and confirm user consent before analysis. <br>
Risk: Cloud history access and local credential or profile storage may expose account-scoped data. <br>
Mitigation: Review stored smyx tokens and profile data before deployment, restrict account access, and clear local data when it is no longer needed. <br>
Risk: Respiratory-rate alerts could be mistaken for medical diagnosis. <br>
Mitigation: Present results as objective monitoring guidance only and direct users to veterinary care for diagnosis or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-pet-carrier-respiratory-rate-analysis) <br>
- [API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown reports and JSON-style API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include respiratory rate, rhythm assessment, threshold status, abnormal feature flags, risk reminders, saved output files, and Markdown tables linking to cloud-hosted historical reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
