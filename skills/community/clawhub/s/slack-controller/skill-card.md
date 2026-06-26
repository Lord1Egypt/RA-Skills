## Description: <br>
Control Slack via Browser Automation to send messages, manage huddles, screen share, set status, and react as the logged-in user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adeel-powerhouse](https://clawhub.ai/user/adeel-powerhouse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and Slack workspace users use this skill to automate Slack actions as their logged-in account, including messaging, huddles, screen sharing, status changes, file uploads, reactions, and search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Slack messages, upload files, start huddles, and share the screen as the logged-in user. <br>
Mitigation: Require explicit confirmation before messages, uploads, huddles, or screen sharing, and verify the target workspace, channel, user, and content before execution. <br>
Risk: Screen sharing and file upload actions may expose sensitive local files or private screen contents. <br>
Mitigation: Close sensitive windows, limit accessible file paths, and use a dedicated automation profile or controlled workspace before sharing or uploading. <br>
Risk: Broad browser or desktop automation has limited built-in scoping safeguards. <br>
Mitigation: Run the skill only in trusted sessions, avoid unattended operation, and keep manual review in the loop for high-impact Slack actions. <br>


## Reference(s): <br>
- [Slack Controller on ClawHub](https://clawhub.ai/adeel-powerhouse/slack-controller) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and action parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates Slack as the logged-in user and may require Slack or Chrome login plus macOS Screen Recording and Accessibility permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
