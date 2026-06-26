## Description: <br>
Sends iMessages through the macOS Messages app with AppleScript for a supplied phone number and message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dezhihe91](https://clawhub.ai/user/dezhihe91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using a macOS agent can ask it to send an iMessage or SMS through Messages after confirming the recipient number and exact message body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause a real outbound iMessage or SMS to be sent from the user's Mac. <br>
Mitigation: Require the agent to show the final recipient number and exact message body before each send. <br>
Risk: Untrusted or unsanitized message text could break AppleScript quoting. <br>
Mitigation: Avoid sending untrusted text directly and review or escape message content before running the AppleScript command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dezhihe91/send-imessage) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash and AppleScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Messages to be signed in; the phone number and message body should be reviewed before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
