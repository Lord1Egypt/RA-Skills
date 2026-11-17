## Description:

Helps agents manage Zoho Projects projects, tasks, milestones, tasklists, and collaboration through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to ask an agent to find and manage Zoho Projects work, including projects, tasks, tasklists, milestones, and time tracking. Developers can also set up approved workflows through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account can grant access beyond the immediate task.

Mitigation: Confirm the connection with the user and review OAuth scopes; prefer read-only access where possible.

Risk: Writes and automated workflows can change or delete project data without the intended review.

Mitigation: Default to read-only operations and obtain separate approval for each write or automation step.

Risk: Using a raw API key can expose a long-lived credential.

Mitigation: Use the Maton CLI when available; avoid the MATON_API_KEY fallback unless the CLI cannot be used.

## Reference(s):

- [Zoho Projects API V3 Documentation](https://projects.zoho.com/api-docs)
- [Zoho Projects Developer Portal](https://www.zoho.com/projects/help/rest-api/zohoprojectsapi.html)
- [Maton Documentation](https://docs.maton.ai)
- [Maton API Reference](https://docs.maton.ai/api-reference/overview)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with CLI, API, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require network access and an authorized Maton connection to Zoho Projects.]

## Skill Version(s):

1.2.7 (source: ClawHub release evidence; skill metadata lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
