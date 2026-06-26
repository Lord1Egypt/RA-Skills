## Description: <br>
Interact with a Vikunja task management instance via its REST API to manage tasks, projects, labels, assignees, reminders, and task relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seergs](https://clawhub.ai/user/seergs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent manage Vikunja tasks and projects through a configured Vikunja instance. It supports common task-management workflows such as listing due work, creating and updating tasks, assigning users, managing labels and reminders, and linking related tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Vikunja API token can allow the agent to read or modify task-management data. <br>
Mitigation: Use the least-privileged Vikunja API token available and rotate it according to the user's normal credential policy. <br>
Risk: A misconfigured base URL could direct requests to the wrong Vikunja instance. <br>
Mitigation: Verify VIKUNJA_BASE_URL before use, especially when working with multiple Vikunja environments. <br>
Risk: Generic task requests can be routed to Vikunja unexpectedly when the user has multiple task systems. <br>
Mitigation: Ask for clarification or explicitly name Vikunja when the intended task system is ambiguous. <br>


## Reference(s): <br>
- [Vikunja API endpoint reference](references/endpoints.md) <br>
- [Project homepage](https://github.com/seergs/vikunja-skill) <br>
- [ClawHub skill page](https://clawhub.ai/seergs/vikunja-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Text, Markdown] <br>
**Output Format:** [Markdown task summaries and REST API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIKUNJA_BASE_URL and VIKUNJA_API_TOKEN.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
