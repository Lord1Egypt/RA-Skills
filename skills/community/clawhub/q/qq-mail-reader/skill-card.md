## Description:

Reads QQ Mail messages over IMAP, handles multiple email encodings, and helps an agent inspect recent or filtered mailbox messages when the user asks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaviwayne](https://clawhub.ai/user/zaviwayne)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to connect to a configured QQ Mail inbox, search recent messages, decode message headers and bodies, and filter mail by user-requested criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic requests to check recent or new mail could authorize access to the configured private QQ inbox.

Mitigation: Install only when mailbox access is intended, and confirm the user's mailbox-access intent before reading or filtering messages.

Risk: The QQ Mail authorization code is sensitive and could expose mailbox contents if stored or shared insecurely.

Mitigation: Store MAIL_USER and MAIL_PASS only in ~/.openclaw/secrets/mail_qq.env, keep that file owner-readable only, and do not commit or share the authorization code.

## Reference(s):

- [QQ Mail IMAP Help](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)
- [ClawHub skill page](https://clawhub.ai/zaviwayne/skills/qq-mail-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAIL_USER and MAIL_PASS in ~/.openclaw/secrets/mail_qq.env before mailbox access.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
