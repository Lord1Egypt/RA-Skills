## Description: <br>
Interact with Zoho CRM, Projects, and Meeting APIs to manage deals, contacts, leads, tasks, projects, milestones, meeting recordings, and related Zoho workspace data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shreefentsar](https://clawhub.ai/user/shreefentsar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, operators, and developers use this skill to let an agent query and update Zoho CRM and Projects records, inspect project work, and retrieve or summarize Zoho Meeting recordings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad long-lived Zoho OAuth access can expose CRM, Projects, Meeting, and file data if credentials are over-scoped or leaked. <br>
Mitigation: Use a dedicated least-privilege Zoho OAuth app, request only the scopes needed for the workflow, and protect the refresh token as a secret. <br>
Risk: CRM and Projects commands can create, update, or delete business records. <br>
Mitigation: Require explicit human confirmation before write or delete actions and review the target module, record ID, and payload before execution. <br>
Risk: Meeting recordings may contain sensitive participant or organizational information and can be sent to Google Gemini for transcription. <br>
Mitigation: Run the summarizer only for recordings approved for third-party transcription by the organization and participants. <br>
Risk: The release evidence notes that the Zoho CLI wrapper source needs review before trust is established. <br>
Mitigation: Review the installed CLI wrapper source and executable path before granting credentials or running API operations. <br>


## Reference(s): <br>
- [Zoho CRM API Reference](references/crm-api.md) <br>
- [Zoho Projects API Reference](references/projects-api.md) <br>
- [Zoho Meeting API Reference](references/meeting-api.md) <br>
- [Zoho API Console](https://api-console.zoho.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/shreefentsar/zoho) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The meeting summarizer can download recordings, transcribe audio through Gemini, and emit structured JSON results for downstream summarization.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
