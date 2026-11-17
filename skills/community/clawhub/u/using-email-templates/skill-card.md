## Description:

Helps agents create, send, and troubleshoot Mailtrap-hosted email templates with Handlebars personalization, template UUID payloads, and sandbox preview workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email teams use this skill to integrate Mailtrap-hosted templates into transactional or bulk email flows, generate responsive email-template HTML, and validate template variables before live sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live or bulk email sends can be externally visible and may reach real recipients.

Mitigation: Use Mailtrap sandbox and testing flows before sending real messages, especially for risky template or variable changes.

Risk: API tokens can be exposed if copied into code, template content, or shared logs.

Mitigation: Keep MAILTRAP_API_TOKEN scoped and stored in environment variables, and avoid embedding secrets in generated examples.

Risk: Outdated SDK method signatures or guessed API request shapes can cause failed sends or incorrect payloads.

Mitigation: Check the relevant SDK README and official Mailtrap API documentation before generating SDK code or request bodies.

## Reference(s):

- [Mailtrap Templates API](https://docs.mailtrap.io/developers/templates/templates.md)
- [Transactional Send Email](https://docs.mailtrap.io/developers/email-sending/transactional.md)
- [Bulk Send Email](https://docs.mailtrap.io/developers/email-sending/bulk.md)
- [Using Handlebars with Email Templates](https://docs.mailtrap.io/email-api-smtp/email-templates/handlebars.md)
- [Testing Templates with Handlebars](https://docs.mailtrap.io/email-api-smtp/email-templates/handlebars.md#testing-templates-with-handlebars)
- [Send Test Emails (Sandbox)](https://docs.mailtrap.io/developers/email-sandbox/send-test-emails.md)
- [Mailtrap Node.js SDK](https://github.com/mailtrap/mailtrap-nodejs)
- [Mailtrap Python SDK](https://github.com/mailtrap/mailtrap-python)
- [Mailtrap PHP SDK](https://github.com/mailtrap/mailtrap-php)
- [Mailtrap Ruby SDK](https://github.com/mailtrap/mailtrap-ruby)
- [Mailtrap Java SDK](https://github.com/mailtrap/mailtrap-java)
- [Mailtrap .NET SDK](https://github.com/mailtrap/mailtrap-dotnet)
- [Mailtrap CLI](https://github.com/mailtrap/mailtrap-cli)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request bodies, SDK usage notes, Handlebars template guidance, and responsive email HTML.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
