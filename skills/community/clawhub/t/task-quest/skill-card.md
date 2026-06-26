## Description: <br>
Task Quest adds a local XP, levels, streaks, and achievements layer to completed smart-tasks work with no manual input required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgkim311](https://clawhub.ai/user/dgkim311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and task-management users with smart-tasks use this skill to make task completion more motivating by tracking XP, levels, streaks, achievements, and brief quest status updates in the agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup and integration can create task-quest files and propose changes to cron prompts, AGENTS.md, and HEARTBEAT.md. <br>
Mitigation: Review the init script and integration diffs before applying them, and only approve workspace changes that match the intended task workflow. <br>
Risk: Disable behavior has documentation inconsistencies around whether active:false stops all tracking or preserves tracking for later reactivation. <br>
Mitigation: Decide explicitly whether active:false should stop all tracking in the workspace, and verify agent instructions reflect that decision. <br>


## Reference(s): <br>
- [Task Quest ClawHub listing](https://clawhub.ai/dgkim311/task-quest) <br>
- [Task Quest publisher profile](https://clawhub.ai/user/dgkim311) <br>
- [Mechanics reference](artifact/references/mechanics.md) <br>
- [Achievements reference](artifact/references/achievements.md) <br>
- [Themes reference](artifact/references/themes.md) <br>
- [Workspace integration guide](artifact/references/workspace-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline status text, shell commands, and YAML/Markdown workspace state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local task-quest state files after setup; companion skill for smart-tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
