## Description:

Send iMessages or SMS-like messages through the macOS Messages app using AppleScript when a user provides a recipient phone number and message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dezhihe91](https://clawhub.ai/user/dezhihe91)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft and execute macOS Messages AppleScript commands for sending a specified message to a specified phone number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real messages from the user's account without a required confirmation step.

Mitigation: Use only where the agent shows the exact recipient and message body and receives explicit user approval before sending.

Risk: The AppleScript instructions embed user-provided phone numbers and message text into generated script text.

Mitigation: Prefer passing the phone number and message as AppleScript arguments or otherwise safely escaping generated script values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dezhihe91/skills/send-imessage)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and AppleScript command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Messages to be signed in and able to send messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
