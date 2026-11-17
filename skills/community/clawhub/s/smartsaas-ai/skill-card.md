## Description:

SmartSaaS helps agents manage SmartSaaS datasets, projects, tasks, knowledge, campaigns, templates, integrations, events, and cron workflows through bundled shell scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smartsaas](https://clawhub.ai/user/smartsaas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run SmartSaaS administrative workflows from an agent, including creating datasets, adding dataset items, managing projects and tasks, working with knowledge articles, templates, campaigns, integrations, webhooks, and cron jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a broad SmartSaaS admin connector with account mutation rights.

Mitigation: Install it only with a least-privilege SmartSaaS API key and review requested actions before execution.

Risk: Unsafe script behavior could expose the API key or run unintended local code.

Mitigation: Review the bundled scripts before installation and avoid passing untrusted values to script arguments.

Risk: Name-based dataset lookup can target the wrong dataset.

Mitigation: Use dataset folder IDs whenever adding items and avoid name-based dataset lookup until it is fixed.

Risk: Production HTTPS requests need normal TLS verification.

Mitigation: Require normal TLS verification for production URLs and avoid workflows that disable certificate checks outside local development.

Risk: Integration removal, campaign start, email send, webhook, and cron operations can cause external side effects.

Mitigation: Require explicit user confirmation before running those operations.

## Reference(s):

- [SmartSaaS ClawHub release](https://clawhub.ai/smartsaas/skills/smartsaas-ai)
- [SmartSaaS artifact documentation](artifact/SMARTSAAS.md)
- [Dataset schema](artifact/schemas/dataset.json)
- [Task schema](artifact/schemas/task.json)
- [Campaign schema](artifact/schemas/campaign.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with shell command invocations and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute bundled shell scripts that call the SmartSaaS API when the required environment variables are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
