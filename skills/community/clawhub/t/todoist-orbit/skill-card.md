## Description: <br>
Operate Todoist through a deterministic Python CLI backed by the Todoist REST API for task, project, section, label, comment, and attachment automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myx0m0p](https://clawhub.ai/user/myx0m0p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run deterministic Todoist REST API workflows from a Python CLI, including task, project, section, label, comment, and attachment operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change, delete, close, archive, and upload data in the user's Todoist account. <br>
Mitigation: Install only when Todoist account management is intended, keep the API token private, and verify target IDs before update, archive, delete, or close commands. <br>
Risk: File, stdin, or comment content can be uploaded to Todoist. <br>
Mitigation: Review file and stdin content before upload, and use file or stdin based comment commands for longer material. <br>
Risk: Some Todoist features vary by account or workspace plan, especially upload and comment behavior. <br>
Mitigation: Check command JSON results and handle Todoist API errors before relying on an operation as completed. <br>


## Reference(s): <br>
- [Todoist Orbit API notes](references/api-notes.md) <br>
- [Todoist REST API base](https://api.todoist.com/api/v1) <br>
- [Todoist developer token settings](https://todoist.com/app/settings/integrations/developer) <br>
- [ClawHub skill page](https://clawhub.ai/myx0m0p/todoist-orbit) <br>
- [Publisher profile](https://clawhub.ai/user/myx0m0p) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TODOIST_API_KEY; --pretty enables indented JSON output.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
