## Description: <br>
Control a Toggl Track workspace via CLI commands for time entries, projects, clients, tasks, tags, workspaces, organizations, groups, and user profile data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FroeMic](https://clawhub.ai/user/FroeMic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to install and operate a Toggl CLI that starts and stops timers, lists records, and manages Toggl Track workspace objects from shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install external Node code that was not reviewed in the supplied evidence. <br>
Mitigation: Review the external toggl-cli repository and dependencies before installing, and pin a trusted commit when possible. <br>
Risk: The Toggl API token is a long-lived secret that can expose workspace data if mishandled. <br>
Mitigation: Store TOGGL_API_TOKEN only where local file permissions are appropriate, avoid sharing it in prompts or logs, and rotate it if exposed. <br>
Risk: The documented commands can create, update, archive, restore, delete, start, or stop records in a real Toggl workspace. <br>
Mitigation: Require explicit confirmation before running write actions against production Toggl data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FroeMic/toggl-cli) <br>
- [toggl-cli repository cited by the skill](https://github.com/FroeMic/toggl-cli) <br>
- [Toggl Track profile settings](https://track.toggl.com/profile) <br>
- [Toggl Track API v9 base URL](https://api.track.toggl.com/api/v9) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI commands and environment variable setup for TOGGL_API_TOKEN and optional TOGGL_WORKSPACE_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
