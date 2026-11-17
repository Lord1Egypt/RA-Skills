## Description:

Interact with YouTrack project management system via REST API to read projects and issues, create tasks, generate invoices from time tracking data, and manage knowledge base articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[digisal](https://clawhub.ai/user/digisal)

### License/Terms of Use:


## Use Case:

Developers, project managers, and operations teams use this skill to work with YouTrack projects, issues, time tracking, invoices, and knowledge base articles through REST API-backed helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a permanent YouTrack API token.

Mitigation: Use a least-privilege token, store it in a protected environment variable or secret manager, and avoid passing it through the --token argument.

Risk: The scripts connect to a user-supplied YouTrack URL with weak destination checks.

Mitigation: Verify the URL is the intended HTTPS YouTrack host before running any API operation.

Risk: Generated invoices may expose sensitive project data.

Mitigation: Treat invoice files as sensitive and redact internal issue descriptions, author names, and work-log details before external sharing.

## Reference(s):

- [YouTrack API References](REFERENCES.md)
- [ClawHub Skill Page](https://clawhub.ai/digisal/skills/youtrack-digisal)
- [Publisher Profile](https://clawhub.ai/user/digisal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell examples; scripts can emit plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Invoice output may include internal issue descriptions, author names, and work-log details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
