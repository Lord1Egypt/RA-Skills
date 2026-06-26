## Description: <br>
Manage Userorbit resources via the public API. Create and manage feedback, announcements, roadmap topics, help center articles, boards, tags, subscribers, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[middlerange](https://clawhub.ai/user/middlerange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect, create, update, publish, archive, restore, and delete Userorbit feedback, announcements, roadmaps, help center content, subscribers, projects, tags, and related resources through the Userorbit REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on live Userorbit business content and customer-facing resources. <br>
Mitigation: Use a least-privileged API key and require explicit approval before publish, delete, archive, restore, subscriber, project, or bulk update actions. <br>
Risk: Credentials are required for API calls. <br>
Mitigation: Provide USERORBIT_API_KEY and USERORBIT_TEAM_ID through environment variables only, and keep them out of chat, command output, and logs. <br>


## Reference(s): <br>
- [Userorbit skill page](https://clawhub.ai/middlerange/userorbit) <br>
- [Userorbit API reference](references/api.md) <br>
- [Userorbit API base URL](https://api.userorbit.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires USERORBIT_API_KEY and USERORBIT_TEAM_ID environment variables.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
