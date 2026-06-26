## Description: <br>
Manage Todoist tasks, projects, labels, and comments via the Todoist CLI wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreisuslov](https://clawhub.ai/user/andreisuslov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Todoist tasks, projects, sections, labels, and comments through a local Todoist CLI wrapper backed by the Todoist REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a sensitive Todoist API token to a CLI helper that was referenced but not included for review. <br>
Mitigation: Inspect and trust the exact todoist executable before use, provide the token through a temporary environment variable or secret manager, and rotate the token if it may have been exposed. <br>
Risk: The documented commands can complete, reopen, update, or delete Todoist tasks, projects, labels, sections, and comments. <br>
Mitigation: Confirm target IDs and names before running mutating commands, especially update, complete, reopen, and delete operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andreisuslov/todoist-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Todoist CLI commands require TODOIST_API_TOKEN plus curl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
