## Description: <br>
Starts and completes WordPress.com OAuth, validates token health, and publishes draft or published posts through the WordPress.com REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibrahimelnemr](https://clawhub.ai/user/ibrahimelnemr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to run a human-in-the-loop WordPress.com OAuth flow, store the resulting bearer token, check token validity, and publish posts to a WordPress.com or Jetpack-connected site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The stored WordPress access token can grant access to the connected site if exposed. <br>
Mitigation: Install only when the publisher is trusted, keep credentials.json out of source control, sync folders, logs, and backups, and delete the stored credentials or revoke the token when it is no longer needed. <br>
Risk: Publishing with a valid token can create live site content. <br>
Mitigation: Use draft status for first tests and review posts before publishing them publicly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibrahimelnemr/wordpress-oauth) <br>
- [Publisher profile](https://clawhub.ai/user/ibrahimelnemr) <br>
- [WordPress.com OAuth authorize endpoint](https://public-api.wordpress.com/oauth2/authorize) <br>
- [WordPress.com OAuth token endpoint](https://public-api.wordpress.com/oauth2/token) <br>
- [WordPress.com token-info endpoint](https://public-api.wordpress.com/oauth2/token-info) <br>
- [WordPress.com post publishing endpoint](https://public-api.wordpress.com/rest/v1.1/sites/{site}/posts/new) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes OAuth state and credential JSON files in the skill directory when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
