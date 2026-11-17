## Description:

Redmine Pilot integrates with the Redmine REST API to help agents query issues, create issues, update issue status, list projects, and search tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zer07z](https://clawhub.ai/user/zer07z)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to manage Redmine project work from an agent, including issue lookup, issue creation, issue updates, project listing, and metadata retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Redmine API key to read or change project data.

Mitigation: Use a least-privilege API key, prefer HTTPS Redmine URLs, avoid broad production credentials, and review create or update actions before execution.

Risk: The configured Redmine server URL determines where credentials and requests are sent.

Mitigation: Install only when the Redmine server URL is trusted and verify the configured endpoint before using the skill.

## Reference(s):

- [Redmine data structure example](references/schema-example.md)
- [Redmine Pilot on ClawHub](https://clawhub.ai/zer07z/skills/redmine-pilot)
- [zer07z publisher profile](https://clawhub.ai/user/zer07z)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Redmine REST API through curl examples or the bundled Python script when configured with a Redmine URL and API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
