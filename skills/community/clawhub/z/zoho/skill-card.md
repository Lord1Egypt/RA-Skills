## Description:

Interact with Zoho CRM, Projects, and Meeting APIs. Use when managing deals, contacts, leads, tasks, projects, milestones, meeting recordings, or any Zoho workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shreefentsar](https://clawhub.ai/user/shreefentsar)

### License/Terms of Use:

MIT

## Use Case:

Employees, operators, and developers use this skill to let an agent query and update Zoho CRM records, manage Zoho Projects work items, and retrieve Zoho Meeting recordings for transcription and summary workflows.

### Deployment Geography for Use:

Global, subject to the configured Zoho datacenter and the organization's data handling requirements.

## Known Risks and Mitigations:

Risk: The OAuth scopes shown for setup can grant broad read/write access to CRM and Projects data.

Mitigation: Request only the Zoho scopes needed for the intended workflow and review high-impact write operations before execution.

Risk: The skill uses long-lived Zoho credentials and a Gemini API key.

Mitigation: Store secrets in a managed secret store or protected environment variables instead of a skill-directory .env file.

Risk: Examples include destructive or business-impacting operations such as deleting CRM records and updating project tasks.

Mitigation: Require explicit user approval for creates, updates, deletes, meeting downloads, and other irreversible actions.

Risk: Meeting recordings may be downloaded and sent to Gemini for transcription.

Mitigation: Run transcription only when participants and data owners are authorized for third-party processing of the recording.

Risk: Security guidance notes that the package should include or clearly declare the required Zoho CLI wrapper dependency.

Mitigation: Verify that the installed package contains the executable CLI wrapper or document the external dependency before use.

## Reference(s):

- [ClawHub Zoho skill page](https://clawhub.ai/shreefentsar/skills/zoho)
- [Zoho API Console](https://api-console.zoho.com/)
- [Zoho CRM API Reference](references/crm-api.md)
- [Zoho Projects API Endpoints](references/projects-api.md)
- [Zoho Meeting API Reference](references/meeting-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Zoho API results, task or record payloads, recording metadata, transcripts, and meeting summaries.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
