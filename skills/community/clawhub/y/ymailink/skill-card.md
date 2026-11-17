## Description:

Terminal email client guidance for managing, configuring, automating, and troubleshooting email workflows from the command line with ymailink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2969192546](https://clawhub.ai/user/2969192546)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation agents use this skill to install and operate ymailink for reading, sending, organizing, composing, and troubleshooting email from terminal workflows. It also covers account configuration, OAuth and credential handling, attachments, templates, and AI-assisted summaries or reply suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags mutable remote install guidance and a suspicious security verdict.

Mitigation: Install only a trusted version or commit, preferably in a virtual environment, and avoid the Gitee mirror unless it is verified against the intended upstream.

Risk: ymailink configuration files, OAuth token caches, and AI API keys can contain sensitive credentials.

Mitigation: Treat ~/.config/ymailink files as sensitive and prefer keyring or pass over plaintext passwords.

Risk: Email commands can send messages or delete and purge mailbox content.

Mitigation: Review target account, folder, message IDs, and command intent before running send, delete, expunge, or purge operations.

Risk: AI summary and reply commands send email content to an AI endpoint.

Mitigation: Do not use AI features on confidential or regulated email unless the endpoint and its data handling are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2969192546/skills/ymailink)
- [Project homepage](https://github.com/lizhisec/ymailink)
- [Configuration reference](artifact/references/configuration.md)
- [Message composition reference](artifact/references/message-composition.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, TOML configuration snippets, and RFC 822 message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-output command guidance when ymailink is used with --output json.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
