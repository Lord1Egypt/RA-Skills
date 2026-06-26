## Description: <br>
Send and manage iMessages via BlueBubbles self-hosted macOS server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent send and manage iMessage conversations through a self-hosted BlueBubbles server. It supports text messages, attachments, reactions, edits, unsend actions, and iMessage effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send and manage real iMessages through a trusted BlueBubbles server. <br>
Mitigation: Install only when the user operates and trusts the BlueBubbles server, and confirm recipients, message content, attachments, reactions, edits, and unsend actions before execution. <br>
Risk: A broad sender allowlist can permit unintended message handling. <br>
Mitigation: Replace allowed_senders = ["*"] with specific trusted handles whenever possible. <br>
Risk: The BlueBubbles server password grants access to messaging actions. <br>
Mitigation: Keep the server password secret, use HTTPS where possible, and avoid exposing the password in logs, chat output, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/tc-bluebubbles) <br>
- [BlueBubbles](https://bluebubbles.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and TOML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce message-send requests, attachment-send requests, reaction requests, edit or unsend requests, and setup guidance for BlueBubbles server URL and password configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
