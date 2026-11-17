## Description:

Helps an agent manage Todoist tasks by adding tasks, completing or deleting tasks, assigning due dates and priorities, and navigating projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-mindmarket](https://clawhub.ai/user/ai-mindmarket)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Todoist task creation, task status changes, and project lookup. It is intended for Todoist account workflows that require an API token and careful handling of task data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a plaintext Todoist token.

Mitigation: Remove the packaged token, rotate the exposed credential, and require users to provide their own token through a documented secure configuration path.

Risk: Documentation understates that the script can perform live Todoist API operations.

Mitigation: Document the live API behavior clearly before installation or execution, including account access scope and expected network calls.

Risk: The script can delete tasks and sync broad account data.

Mitigation: Require explicit confirmation before destructive operations and disable broad sync by default.

Risk: The script exposes task content and identifiers in console output.

Mitigation: Review logging behavior and avoid printing sensitive task data unless the user explicitly requests diagnostic output.

## Reference(s):

- [Todoist API v2 endpoint](https://api.todoist.com/api/v2)
- [Security and Privacy Guidelines](references/SECURITY.md)
- [API Configuration](references/API_CONFIG.json)
- [Publisher profile](https://clawhub.ai/user/ai-mindmarket)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text]

**Output Format:** [Markdown guidance with inline shell commands and console text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Todoist API token and may perform live account operations when the script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
