## Description:

Send Signal messages and look up Signal recipients via the local signal-cli installation on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pseudobun](https://clawhub.ai/user/pseudobun)

### License/Terms of Use:


## Use Case:

Users and agents use this skill to resolve Signal contacts and send Signal text messages or attachments through a local, already registered signal-cli installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send messages through the user's local Signal account.

Mitigation: Confirm the exact recipient and final message text with the user before sending.

Risk: Error output can expose message text, phone numbers, or attachment paths.

Mitigation: Avoid highly sensitive messages unless error logging is reviewed and redacted.

Risk: Name-based recipient resolution can return ambiguous matches.

Mitigation: Present matching candidates and ask the user to choose the intended recipient before sending.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local signal-cli setup and user confirmation before sending messages.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
