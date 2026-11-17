## Description:

Send transactional and marketing emails via UniOne Email API, manage email templates, validate email addresses, check delivery statistics, manage suppression lists, configure webhooks, and handle domain settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unione-repo](https://clawhub.ai/user/unione-repo)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and marketing teams use this skill to guide agents through UniOne email delivery tasks, including sending transactional or marketing messages, validating addresses, managing templates, configuring webhooks, checking domains, and handling suppressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A production UniOne API key could send email or change real account resources.

Mitigation: Use a narrowly scoped key stored in an environment variable or secret manager, and require explicit approval before any send, create, update, subscribe, or delete action.

Risk: Deletion or modification of templates, webhooks, suppressions, tags, projects, or event dumps can affect delivery operations and reporting.

Mitigation: Show the exact target and planned change before execution, then wait for user confirmation.

Risk: Unverified sending domains can prevent delivery or cause failed sends.

Mitigation: Check domain status before sending and guide users to add DNS records at their DNS provider themselves.

## Reference(s):

- [UniOne Website](https://unione.io/en/)
- [UniOne API Documentation](https://docs.unione.io/en/web-api-ref)
- [UniOne Getting Started](https://docs.unione.io/en/)
- [Template Engines](https://docs.unione.io/en/web-api#section-template-engines)
- [ClawHub Skill Page](https://clawhub.ai/unione-repo/skills/unione-api-skill)
- [Publisher Profile](https://clawhub.ai/user/unione-repo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UniOne API request bodies, curl commands, language-specific snippets, DNS record guidance, and confirmation prompts.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
