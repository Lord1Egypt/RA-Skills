## Description:

Use when integrating, configuring, or troubleshooting Mailtrap live email sending (Email API or SMTP). Use when wiring outbound mail from an application or choosing how to send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill when integrating, configuring, or troubleshooting Mailtrap live email sending through Email API, SMTP, SDKs, plugins, batch sends, or bulk streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples may send live email when run with valid Mailtrap credentials.

Mitigation: Review generated send commands before running them and test first with sandbox or verified test recipients.

Risk: Mailtrap API tokens could be exposed or over-permissioned if copied into code or command history.

Mitigation: Keep the API token scoped and store it in environment variables or a secrets manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mailtrap/skills/sending-emails)
- [Mailtrap transactional email sending documentation](https://docs.mailtrap.io/developers/email-sending/transactional.md)
- [Mailtrap bulk email sending documentation](https://docs.mailtrap.io/developers/email-sending/bulk.md)
- [Mailtrap suppressions documentation](https://docs.mailtrap.io/developers/email-sending/suppressions.md)
- [Mailtrap Node.js SDK](https://github.com/mailtrap/mailtrap-nodejs)
- [Mailtrap Python SDK](https://github.com/mailtrap/mailtrap-python)
- [Mailtrap PHP SDK](https://github.com/mailtrap/mailtrap-php)
- [Mailtrap Ruby SDK](https://github.com/mailtrap/mailtrap-ruby)
- [Mailtrap Java SDK](https://github.com/mailtrap/mailtrap-java)
- [Mailtrap .NET SDK](https://github.com/mailtrap/mailtrap-dotnet)
- [Mailtrap CLI](https://github.com/mailtrap/mailtrap-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API, SMTP, SDK, configuration, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live-send examples that require review before execution with valid Mailtrap credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
