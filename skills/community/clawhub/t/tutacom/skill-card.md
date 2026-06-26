## Description: <br>
Send, read, and manage emails via Tuta (formerly Tutanota) encrypted email service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIDidMyHomework](https://clawhub.ai/user/AIDidMyHomework) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check a Tuta inbox, read email, and send non-confidential email to external recipients through a Tuta account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access mailbox contents and send mail from the user's Tuta account. <br>
Mitigation: Install only when the publisher is trusted with full mailbox and send access, and manually confirm recipients, subject, and body before any send action. <br>
Risk: Reusable decrypted mail keys are stored in a local session file. <br>
Mitigation: Use a private session-file path instead of /tmp when possible and delete the session file after use. <br>
Risk: Account credentials are configured through openclaw.json. <br>
Mitigation: Protect openclaw.json and avoid exposing it in shared workspaces, logs, or version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIDidMyHomework/tutacom) <br>
- [Tuta REST endpoint](https://app.tuta.com/rest/) <br>
- [Tutanota client reference implementation](https://github.com/nenaddi/tutanota_client) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output with concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through a local Tuta session file and can read mailbox contents or send external email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
