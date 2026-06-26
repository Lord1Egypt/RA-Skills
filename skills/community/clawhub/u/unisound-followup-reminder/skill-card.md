## Description: <br>
Provides patient-side chronic disease follow-up and appointment reminders from last-visit dates, follow-up intervals, or specific follow-up dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Care teams or patient-management agents use this skill to calculate follow-up dates, detect overdue chronic-disease appointments, and generate patient-friendly reminder text. It is limited to reminders and does not replace clinician scheduling or medical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patient follow-up details and notes may be sent to a remote medical-model API. <br>
Mitigation: Use only after confirming the provider's privacy, retention, logging, and healthcare compliance terms; prefer minimal structured input for real patient data. <br>
Risk: The app key is a sensitive credential required for model access. <br>
Mitigation: Protect the app key, pass it only through approved secret-handling paths, and avoid storing it in command history, files, or logs. <br>
Risk: Office, PDF, and image inputs can contain excess or incorrectly extracted patient information. <br>
Mitigation: Prefer JSON input when possible and review prepared extracted data before sending it to the remote API. <br>


## Reference(s): <br>
- [Simple app features: appointments and overdue patients](https://docs.simple.org/readme/simple-app-features) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [UTF-8 JSON with structured follow-up data and Markdown reminder text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided app key for the remote medical-model API; optional document and image parsing may require local dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
