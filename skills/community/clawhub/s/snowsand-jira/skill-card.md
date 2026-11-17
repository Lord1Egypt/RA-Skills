## Description:

Interact with Jira Cloud via REST API for searching issues with JQL, viewing issue details, creating and updating issues, adding comments, transitioning status, querying sprints and boards, and logging work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to operate Jira Cloud workflows from an agent, including issue search, issue updates, comments, transitions, sprint queries, and worklog tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live Jira changes, including creating or updating issues, adding comments, transitioning status, and logging work.

Mitigation: Use a narrowly permissioned Jira API token and require explicit approval before any create, update, comment, transition, worklog, raw API, link, or attachment operation.

Risk: Jira API credentials can be sent to the URL configured in JIRA_BASE_URL.

Mitigation: Set JIRA_BASE_URL only to the intended HTTPS Atlassian tenant and review the environment before running authenticated commands.

## Reference(s):

- [Jira Field Reference](references/fields.md)
- [Atlassian Jira Cloud REST API v3 documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate against Jira Cloud REST APIs using environment-provided Jira credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
