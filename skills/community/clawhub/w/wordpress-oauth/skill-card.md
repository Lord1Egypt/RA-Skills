## Description:

Start and complete WordPress.com OAuth and publish posts through the WordPress.com REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibrahimelnemr](https://clawhub.ai/user/ibrahimelnemr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation operators use this skill to complete a human-in-the-loop WordPress.com OAuth flow, validate token health, and publish draft or live posts to WordPress.com or Jetpack-connected sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and handles a reusable WordPress bearer token in its own directory, which could expose publishing access if the directory or credentials file is shared.

Mitigation: Keep the skill directory private, restrict file permissions, and revoke the WordPress token if credentials.json or command logs may have been exposed.

Risk: OAuth client secrets, callback URLs, and bearer tokens may appear in shell history, CI logs, or shared terminals when secret-bearing commands are run.

Mitigation: Avoid running secret-bearing commands in logged shells or CI and prefer environment handling that does not echo secrets.

Risk: The publish command can create public posts when a publish status is selected.

Mitigation: Use the smallest OAuth scope needed and begin with draft status until the integration has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ibrahimelnemr/skills/wordpress-oauth)
- [WordPress.com OAuth Authorization Endpoint](https://public-api.wordpress.com/oauth2/authorize)
- [WordPress.com OAuth Token Endpoint](https://public-api.wordpress.com/oauth2/token)
- [WordPress.com OAuth Token Info Endpoint](https://public-api.wordpress.com/oauth2/token-info)
- [WordPress.com REST Post Creation Endpoint](https://public-api.wordpress.com/rest/v1.1/sites/{site}/posts/new)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores OAuth state and reusable WordPress credentials as local JSON files in the skill directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
