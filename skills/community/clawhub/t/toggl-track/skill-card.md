## Description: <br>
Provides a Toggl Track API integration through Maton-managed OAuth for tracking time and managing projects, clients, workspaces, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent read and manage Toggl Track time entries, projects, clients, workspaces, and tags through an authenticated Maton connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MATON_API_KEY is a bearer secret for the Maton account. <br>
Mitigation: Keep it in an environment variable or secret store, avoid printing or pasting it, and remove it from logs and shared transcripts. <br>
Risk: The skill can create, update, delete, or stop Toggl Track resources and can manage OAuth connections. <br>
Mitigation: Require the agent to show the exact target record, workspace or connection, and intended effect before any write, delete, or connection-changing action. <br>
Risk: Requests may use the wrong Toggl Track account when multiple Maton connections exist. <br>
Mitigation: Specify the intended connection with the Maton-Connection header whenever more than one active Toggl Track connection is available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/toggl-track) <br>
- [Maton](https://maton.ai) <br>
- [Toggl Track API Documentation](https://engineering.toggl.com/docs/) <br>
- [Toggl Track API Reference](https://engineering.toggl.com/docs/api/) <br>
- [Time Entries API](https://engineering.toggl.com/docs/api/time_entries) <br>
- [Projects API](https://engineering.toggl.com/docs/api/projects) <br>
- [Clients API](https://engineering.toggl.com/docs/api/clients) <br>
- [Tags API](https://engineering.toggl.com/docs/api/tags) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Toggl Track OAuth connection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
