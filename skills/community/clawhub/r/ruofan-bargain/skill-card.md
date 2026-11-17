## Description:

Ruofan Bargain Arena helps users join Ruofan's coupon bargaining event and relay bargaining messages to Ruofan's AI shopkeeper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanool](https://clawhub.ai/user/sanool)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to participate in Ruofan's bargain event by providing a passphrase and nickname, sending bargain messages, and reviewing coupon offers returned by the event API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's passphrase, nickname, and bargain messages to ruffood.com, and the resulting conversation may be publicly displayed on the event page.

Mitigation: Ask users to avoid personal or sensitive information in nicknames and bargain messages, and explain that the conversation may become public before sending messages.

Risk: The returned session token controls access to the bargain session.

Mitigation: Treat the session token as private and avoid exposing it in public chat, logs, or shared transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanool/skills/ruofan-bargain)
- [Publisher profile](https://clawhub.ai/user/sanool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with API request examples and conversational status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session token handling guidance, current coupon offer, deal status, remaining rounds, and user-facing privacy reminders.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
