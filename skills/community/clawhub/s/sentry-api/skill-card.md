## Description: <br>
Sentry API integration with managed authentication for monitoring errors, retrieving events, and managing Sentry issues, projects, teams, and releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect Sentry organizations, projects, issues, events, teams, and releases through Maton-managed authentication. It can also guide connection setup and Sentry API request construction when the user has a valid MATON_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton mediates access to the connected Sentry account. <br>
Mitigation: Install only when you trust Maton with that access and review the connected account before use. <br>
Risk: The MATON_API_KEY is a sensitive credential. <br>
Mitigation: Store MATON_API_KEY privately, avoid printing it in logs, and rotate it if exposure is suspected. <br>
Risk: Requests may target the wrong Sentry account when multiple connections exist. <br>
Mitigation: Use the Maton-Connection header to select the intended connection. <br>
Risk: Create, update, and delete operations can change Sentry organizations, projects, teams, issues, releases, or connections. <br>
Mitigation: Require explicit user approval after confirming the exact target resource and intended effect. <br>


## Reference(s): <br>
- [ClawHub Sentry Skill](https://clawhub.ai/byungkyu/sentry-api) <br>
- [Maton](https://maton.ai) <br>
- [Sentry API Documentation](https://docs.sentry.io/api/) <br>
- [Sentry API Authentication](https://docs.sentry.io/api/auth/) <br>
- [Sentry Events API](https://docs.sentry.io/api/events/) <br>
- [Sentry Projects API](https://docs.sentry.io/api/projects/) <br>
- [Sentry Organizations API](https://docs.sentry.io/api/organizations/) <br>
- [Sentry Teams API](https://docs.sentry.io/api/teams/) <br>
- [Sentry Releases API](https://docs.sentry.io/api/releases/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Sentry account through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
