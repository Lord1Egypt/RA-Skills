## Description: <br>
Fetch and analyze issues from Sentry error tracking. Use when asked to check Sentry errors, pull issues, investigate exceptions, review error trends, or get crash reports from a Sentry project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dave-b-b](https://clawhub.ai/user/dave-b-b) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Sentry project issues, query error trends, and retrieve issue details while diagnosing exceptions or crash reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Sentry token can grant read access to project issue and event data. <br>
Mitigation: Use a least-privilege token scoped only to the projects the agent is allowed to inspect, and prefer SENTRY_AUTH_TOKEN over passing tokens on the command line. <br>
Risk: Detailed issue output can expose stack traces, metadata, tags, user context, browser or OS information, and other diagnostic data. <br>
Mitigation: Use --details only when authorized to view and share raw error-event data, and review outputs before forwarding them outside the authorized team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dave-b-b/sentry-issues) <br>
- [Publisher profile](https://clawhub.ai/user/dave-b-b) <br>
- [Sentry API endpoint](https://sentry.io/api/0) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON issue summaries or details, with Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Detailed output can include stack traces, latest event context, tags, metadata, browser and OS information when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
