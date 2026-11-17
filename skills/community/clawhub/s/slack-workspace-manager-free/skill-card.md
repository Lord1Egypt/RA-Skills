## Description: <br>
Slack Workspace Manager Free helps agents manage Slack messages, channels, files, reminders, and user lookups for personal or small-team workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, small teams, and Slack workspace administrators use this skill to coordinate everyday workspace tasks, including sending or scheduling messages, managing channels, handling files, creating reminders, and looking up user information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for live Slack read/write access through OAuth scopes. <br>
Mitigation: Review requested Slack OAuth scopes before installation, authorize only the intended workspace, and confirm how OAuth tokens are stored and revoked. <br>
Risk: Messages, file uploads, channel changes, reminders, updates, and deletions can change a Slack workspace immediately. <br>
Mitigation: Verify each proposed workspace-changing action and require explicit user confirmation before execution. <br>
Risk: Broad activation language could make the skill available outside explicit Slack management tasks. <br>
Mitigation: Use the skill only for clear Slack workspace management requests and review planned actions before tool execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/slack-workspace-manager-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe Slack workspace actions that should be reviewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
