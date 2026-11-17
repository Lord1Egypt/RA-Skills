## Description:

XingQiao is an information subscription and messaging skill that triggers on the "星桥" prefix and supports natural-language commands for sending, pulling, subscribing to, replying to, and asking questions through a remote service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zp75296383](https://clawhub.ai/user/zp75296383)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interact with the XingQiao messaging platform from an agent session, including publishing messages, retrieving subscribed messages, subscribing to users, replying to messages, and participating in public Q&A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account credentials and user content may be sent over plaintext HTTP.

Mitigation: Avoid sending sensitive content through the skill unless the remote service moves to HTTPS.

Risk: Reusable tokens are stored in a local plaintext config.json file.

Mitigation: Treat config.json as secret material, do not commit or share it, and rotate or delete the token if the file may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zp75296383/skills/xingqiaoskill)
- [Publisher profile](https://clawhub.ai/user/zp75296383)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown and terminal-oriented text with JSON-backed local configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local config.json containing service tokens during initialization.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
