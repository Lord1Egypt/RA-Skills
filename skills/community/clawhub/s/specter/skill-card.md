## Description:

Enrich, search, and manage company and professional data, lists, saved searches, and talent or investor signals using the Specter intelligence platform through the Specter CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[froemic](https://clawhub.ai/user/froemic)

### License/Terms of Use:


## Use Case:

Developers, operators, sales teams, and investment researchers can use this skill to query Specter for company intelligence, professional profiles, curated lists, saved searches, and market signals from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run external CLI code that was flagged as requiring review.

Mitigation: Review the upstream Specter CLI repository before installing and prefer a pinned commit or signed release.

Risk: Specter API keys and business or professional data may be exposed if handled carelessly.

Mitigation: Store the API key in an environment variable, avoid inline --api-key values, and use only data that is allowed to be sent to Specter.

Risk: Delete commands for lists and saved searches can remove user-managed data.

Mitigation: Manually confirm identifiers and intent before running any delete command.

## Reference(s):

- [Specter API Console](https://app.tryspecter.com/settings/api-console)
- [Specter API Base URL](https://app.tryspecter.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/froemic/skills/specter)
- [Publisher profile](https://clawhub.ai/user/froemic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands, configuration notes, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to request JSON, table, or CSV output from the Specter CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
