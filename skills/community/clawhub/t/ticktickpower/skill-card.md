## Description: <br>
Manage TickTick tasks and projects from the command line with OAuth2 auth, batch operations, and rate limit handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hfarazi](https://clawhub.ai/user/hfarazi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage TickTick tasks and projects through a local CLI, including authentication, listing, creation, updates, completion, batch abandonment, and file attachment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores TickTick OAuth credentials and optional browser session cookies locally, and the session cookie should be treated like a password. <br>
Mitigation: Install only when local credential storage is acceptable, keep the credential file private, and avoid adding a session cookie unless attachment upload is required. <br>
Risk: The attachment workflow can upload arbitrary local files to TickTick when a valid session cookie is configured. <br>
Mitigation: Review attachment commands before execution and attach only files the user intentionally wants uploaded. <br>
Risk: The server security verdict is suspicious because the attachment feature uses a browser session cookie outside the OAuth flow. <br>
Mitigation: Require human review before deployment and follow the server guidance for cookie handling and file upload consent. <br>


## Reference(s): <br>
- [TickTick Developer Center](https://developer.ticktick.com/manage) <br>
- [TickTick Open API](https://developer.ticktick.com/api) <br>
- [ClawHub release page](https://clawhub.ai/hfarazi/ticktickpower) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands may read or write TickTick tasks and projects and may upload local files when attachment credentials are configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
