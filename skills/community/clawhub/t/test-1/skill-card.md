## Description: <br>
Provides command guidance and a Node.js helper for QQ group administration through a local NapCat OneBot 11 WebSocket API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare QQ group administration commands for a trusted local OneBot/NapCat bot endpoint. It covers group naming, notices, muting, kicks, administrator changes, message deletion, profile updates, and group information queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad bot-control capability beyond narrow QQ group administration tasks. <br>
Mitigation: Restrict allowed OneBot actions to the specific administrative operations required for the deployment. <br>
Risk: An embedded or reused OneBot access token can grant unintended access to the local bot endpoint. <br>
Mitigation: Remove or rotate embedded tokens and configure credentials through a trusted runtime secret path. <br>
Risk: Privileged actions such as kicks, bans, administrator changes, message deletion, and announcements can disrupt a group if run without approval. <br>
Mitigation: Require explicit human approval before executing privileged group-management actions. <br>
Risk: File parameters using @/path can read sensitive local files into command payloads. <br>
Mitigation: Avoid @/file inputs for sensitive paths and limit file access to reviewed, task-specific files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/test-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke privileged OneBot group-management actions when executed by an agent or user.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
