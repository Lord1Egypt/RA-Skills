## Description: <br>
Manage TickTick tasks (add, list, complete) via the local `tickrs` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidsmorais](https://clawhub.ai/user/davidsmorais) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Linux users use this skill to let an agent list TickTick tasks, create new tasks, complete tasks by ID, and list projects through an authenticated local tickrs CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or complete tasks in the authenticated TickTick account. <br>
Mitigation: Confirm task creation and completion requests before allowing the agent to run mutating commands. <br>
Risk: The TickTick client secret and local CLI session are credentials. <br>
Mitigation: Store credentials only in the intended environment and install the skill only when the local tickrs binary is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidsmorais/ticktick-linux) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from tickrs CLI commands with Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated local tickrs CLI plus TICKTICK_CLIENT_ID and TICKTICK_CLIENT_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
