## Description: <br>
Interacts with Jira Cloud via REST API for JQL searches, issue viewing and editing, comments, status transitions, sprint and board queries, and worklog operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and Jira operators use this skill to inspect and modify Jira Cloud issues, comments, statuses, sprints, boards, and worklogs through documented CLI commands and REST API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live changes to Jira data, including creating and updating issues, adding comments, transitioning statuses, and logging work. <br>
Mitigation: Require explicit review before write operations and use the least-privileged Jira account or token available. <br>
Risk: The skill requires a Jira API token that gives the agent access to Jira Cloud. <br>
Mitigation: Provide credentials only through environment variables, scope the token to the minimum needed access, and rotate it according to organizational policy. <br>
Risk: Raw API calls and broad Jira routing can bypass the narrower command examples. <br>
Mitigation: Review raw request URLs and payloads before execution, and prefer documented script commands with visible issue keys and field values. <br>


## Reference(s): <br>
- [Jira Field Reference](references/fields.md) <br>
- [Atlassian Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/) <br>
- [Snowsand Jira ClawHub Page](https://clawhub.ai/snowsand-enterprises/snowsand-jira) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can call Jira Cloud REST APIs and may return JSON from Jira.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
