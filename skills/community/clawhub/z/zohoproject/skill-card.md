## Description:

Manage Zoho Projects by listing portals and projects, creating and updating tasks, adding comments, logging time, managing milestones, and querying task lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katprotech](https://clawhub.ai/user/katprotech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to issue Zoho Projects V3 API commands for project, task, milestone, and time-log workflows from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Zoho OAuth scopes can expose project, task, milestone, timesheet, and bug-management data beyond the user's immediate need.

Mitigation: Use the narrowest Zoho OAuth scopes available and omit bug-management scope unless the workflow requires it.

Risk: Zoho access tokens, refresh tokens, client IDs, and client secrets may be stored in shared plaintext configuration.

Mitigation: Store credentials in a private secret manager or protected local environment and avoid committing or sharing token values.

Risk: An unvalidated ZOHO_DC value could direct authentication or API calls to an unintended domain.

Mitigation: Validate ZOHO_DC against official Zoho data-center domains before using it in request URLs.

Risk: Write and delete operations can modify or remove Zoho Projects records.

Mitigation: Require explicit user confirmation before task deletion or other destructive writes.

## Reference(s):

- [Zoho Projects API Documentation](https://projects.zoho.com/api-docs)
- [Zoho API Console](https://api-console.zoho.com/)
- [ClawHub Skill Page](https://clawhub.ai/katprotech/skills/zohoproject)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Zoho OAuth credentials and portal, project, task, milestone, and time-log identifiers supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
