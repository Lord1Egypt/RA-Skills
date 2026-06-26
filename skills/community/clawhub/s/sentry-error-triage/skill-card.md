## Description: <br>
Sentry error tracking - list, triage, and resolve issues; manage releases and source maps via CLI and REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect unresolved Sentry issues, fetch event details and stack traces, triage severity, and manage releases, deploys, and source maps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Sentry token to change monitoring state, including resolving, ignoring, assigning, or bulk-updating issues and creating releases or deploys. <br>
Mitigation: Use the narrowest Sentry token scopes possible and require explicit approval before state-changing Sentry actions. <br>
Risk: Sentry events, stack traces, and source maps may contain sensitive application or user data. <br>
Mitigation: Keep tokens out of chats, logs, and shell history, and review fetched events or uploaded artifacts for sensitive data before sharing or storing outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/sentry-error-triage) <br>
- [Sentry REST API base](https://sentry.io/api/0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires sentry-cli plus Sentry organization, project, and auth token configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
