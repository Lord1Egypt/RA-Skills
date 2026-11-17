## Description:

Operate Facebook Messenger safely through a live signed-in Chrome session with remote debugging enabled using Chrome DevTools MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tschonleber](https://clawhub.ai/user/tschonleber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft or send Facebook Messenger messages through a live signed-in Chrome session while verifying the target thread, composer ownership, group-chat context, and send result. It is intended for supervised Messenger workflows where wrong-recipient, ambiguous search, and high-stakes social content need explicit safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read from and send messages in a signed-in Facebook Messenger session.

Mitigation: Install only for operators comfortable with that access, use a dedicated or carefully chosen Chrome profile, and supervise sends.

Risk: Messages can be sent to the wrong thread when search results, active headers, or composer ownership are ambiguous.

Mitigation: Verify the active conversation, composer, and visible thread context after each meaningful UI change, and stop instead of guessing on ambiguity.

Risk: Sensitive, financial, legal, professional, or emotionally high-stakes messages can create social or business harm if sent automatically.

Mitigation: Prefer draft mode and explicit review for high-stakes content, commitments, group chats, or uncertain cases.

## Reference(s):

- [Safe Facebook Messenger on ClawHub](https://clawhub.ai/tschonleber/skills/safe-facebook-messenger)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Plain text operational guidance and Messenger draft/send decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a live signed-in Chrome session with Chrome DevTools MCP connected.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
