## Description: <br>
Helps an agent use Publer API endpoints to manage social posts, media, workspaces, connected accounts, analytics, competitor analysis, and hashtag insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gjeka](https://clawhub.ai/user/Gjeka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and marketing teams use this skill to let an agent prepare Publer API calls for scheduling, publishing, updating, deleting, reviewing, and analyzing social media content. It is most useful when the user already has a Publer Business plan, API key, workspace ID, and target social accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on live social media content when given a Publer API key. <br>
Mitigation: Require the agent to show the target workspace, accounts, post IDs, content, schedule, recurrence, and deletion list before publishing, updating, deleting, or bulk-scheduling content. <br>
Risk: A broad or exposed API key could allow unintended access to Publer workspaces and social media operations. <br>
Mitigation: Provide the API key only when needed, never hardcode or expose it, and use the smallest necessary Publer scopes. <br>
Risk: Asynchronous jobs and partial failures can make a publishing or media operation appear complete before all targets succeeded. <br>
Mitigation: Poll the job status endpoint until completion or failure, inspect partial failures, and summarize the final per-account outcome to the user. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Gjeka/publer-api) <br>
- [Publer API base URL](https://app.publer.com/api/v1) <br>
- [Artifact API reference](artifact/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with HTTP endpoints, headers, parameters, and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may require a user-provided Publer API key, workspace ID, account IDs, post IDs, date ranges, and media identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
