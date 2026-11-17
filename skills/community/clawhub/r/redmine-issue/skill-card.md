## Description:

Read Redmine issues from any Redmine server via REST API with configurable URL and credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoway](https://clawhub.ai/user/guoway)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to retrieve, list, filter, inspect, and update Redmine issues through a configured Redmine REST API endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Redmine credentials that can read and may modify issue data.

Mitigation: Use narrowly scoped credentials, prefer API keys over username/password authentication, and use read-only credentials for planning workflows when updates are not required.

Risk: The documented read-oriented skill also exposes an authenticated update command.

Mitigation: Require an explicit human approval step before agents run update operations that change issue status, assignment, priority, description, subject, done ratio, or notes.

Risk: Credentials and issue data are sent to the configured Redmine server.

Mitigation: Configure only trusted HTTPS Redmine URLs and avoid using this skill against untrusted or non-TLS endpoints.

## Reference(s):

- [Redmine Issue on ClawHub](https://clawhub.ai/guoway/skills/redmine-issue)
- [Publisher profile: guoway](https://clawhub.ai/user/guoway)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON responses from Redmine API operations, with Markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDMINE_URL and either REDMINE_API_KEY or REDMINE_USERNAME plus REDMINE_PASSWORD.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
