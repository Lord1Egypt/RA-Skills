## Description: <br>
Manage Todoist tasks by listing, creating, completing, updating, and organizing tasks and projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fluidiguana](https://clawhub.ai/user/fluidiguana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill as a concise Todoist API v1 reference for authenticated task, project, section, and label workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Todoist personal API token grants account access and can be exposed through shared shells, logs, or prompts. <br>
Mitigation: Set TODOIST_TOKEN only in trusted environments, avoid printing it, and rotate the token if it may have been exposed. <br>
Risk: The documented API operations can create, update, complete, or delete Todoist data. <br>
Mitigation: Require explicit confirmation before mutating Todoist data, and prefer completing tasks over deleting them when appropriate. <br>


## Reference(s): <br>
- [Todoist API v1 base endpoint](https://api.todoist.com/api/v1/) <br>
- [Todoist developer token settings](https://app.todoist.com/app/settings/integrations/developer) <br>
- [ClawHub skill page](https://clawhub.ai/fluidiguana/todoist-v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Todoist personal API token in TODOIST_TOKEN for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
