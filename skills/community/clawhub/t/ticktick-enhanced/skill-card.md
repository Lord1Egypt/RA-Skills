## Description: <br>
Manage TickTick tasks and projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halr9000](https://clawhub.ai/user/halr9000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to list, create, edit, complete, abandon, and triage TickTick tasks and projects from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can immediately create, edit, complete, or abandon remote TickTick tasks. <br>
Mitigation: Review commands before execution and confirm task IDs with list or details output before mutating tasks. <br>
Risk: OAuth credentials and tokens are stored on disk under ~/.clawdbot/credentials/ticktick-cli/. <br>
Mitigation: Install only if the publisher is trusted with TickTick read/write access, protect local credential files, and revoke the OAuth app when no longer using the skill. <br>
Risk: Batch abandon operations can affect multiple tasks at once. <br>
Mitigation: Use batch operations only after verifying every task ID and prefer single-task commands for uncertain changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/halr9000/ticktick-enhanced) <br>
- [TickTick Open API Endpoint](https://api.ticktick.com/open/v1) <br>
- [TickTick OAuth Endpoint](https://ticktick.com/oauth) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, yaml, configuration] <br>
**Output Format:** [Terminal text with optional JSON or YAML command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read and immediately change remote TickTick task data.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence; CLI command metadata also reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
