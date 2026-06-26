## Description: <br>
Direct Todoist API integration via curl/jq. Lightweight, reliable, and uses working v1/v2 endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NitsujY](https://clawhub.ai/user/NitsujY) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Todoist users use this skill to list, create, complete, and inspect Todoist tasks, projects, and sections through direct Todoist API requests when a CLI is unavailable or failing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todoist API tokens can be exposed through prompts, logs, or copied shell history. <br>
Mitigation: Prefer the TODOIST_API_TOKEN environment variable, keep tokens out of prompts and logs, and rotate tokens if exposure is suspected. <br>
Risk: Create-task and complete-task commands change the user's Todoist account. <br>
Mitigation: Review generated write commands before execution, especially task content, due dates, project IDs, and task IDs. <br>


## Reference(s): <br>
- [Todoist Developer Documentation](https://developer.todoist.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/NitsujY/todoist-api-rest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and TODOIST_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
