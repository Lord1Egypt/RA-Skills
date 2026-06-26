## Description: <br>
Todoist API integration with managed OAuth for reading and managing tasks, projects, sections, labels, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a Todoist account through Maton and ask an agent to list, create, update, complete, or organize Todoist work items. Write actions should be confirmed with the user before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change tasks, projects, sections, labels, and comments in the connected Todoist account. <br>
Mitigation: Keep MATON_API_KEY private and confirm create, update, delete, and complete actions with the user before execution. <br>
Risk: Requests use Maton-managed OAuth to access Todoist, so use depends on trusting Maton with the Todoist connection. <br>
Mitigation: Install only if Maton is trusted for this workflow and revoke or rotate connections and API keys when access should end. <br>
Risk: If multiple Todoist connections exist, requests could target the wrong account. <br>
Mitigation: Specify the intended connection when more than one active Todoist connection is available. <br>


## Reference(s): <br>
- [ClawHub Todoist skill page](https://clawhub.ai/byungkyu/todoist-api) <br>
- [Todoist API v1 documentation](https://developer.todoist.com/api/v1) <br>
- [Todoist filter syntax](https://todoist.com/help/articles/introduction-to-filters) <br>
- [Todoist OAuth documentation](https://developer.todoist.com/guides/#oauth) <br>
- [Maton API key settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with HTTP endpoint references and Python, JavaScript, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user approval for write operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
