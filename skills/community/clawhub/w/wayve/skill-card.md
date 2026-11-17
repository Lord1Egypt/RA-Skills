## Description:

Wayve helps solopreneurs use AI agents for weekly planning, time audits, automation discovery, persistent coaching memory, daily briefs, and life-pillar balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skoppert](https://clawhub.ai/user/skoppert)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an AI agent to the Wayve CLI for solopreneur planning, coaching, time-audit analysis, activity management, knowledge storage, and automation setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the Wayve CLI to read, store, and change sensitive planning, schedule, health, family, coaching, and business context.

Mitigation: Install only after reviewing the integration and use explicit confirmation before saving sensitive memories or changing planning data.

Risk: The skill depends on a floating npm package reference for the Wayve CLI.

Mitigation: Consider pinning the CLI to a reviewed version before use in a controlled or commercial environment.

Risk: Automation setup can involve notification channels and delivery credentials such as bot tokens or webhooks.

Mitigation: Avoid pasting secrets into command lines where possible, confirm channel configuration with the user, and rotate exposed tokens.

## Reference(s):

- [Wayve homepage](https://www.gowayve.com)
- [Wayve CLI setup](https://www.gowayve.com/docs/cli-setup)
- [Setup Guide](references/setup-guide.md)
- [Wayve CLI Command Reference](references/tool-reference.md)
- [Automations](references/automations.md)
- [Knowledge and Learning System](references/knowledge-learning.md)
- [Coaching Playbook](references/coaching-playbook.md)
- [Time Audit](references/time-audit.md)
- [Daily Brief](references/daily-brief.md)
- [Fresh Start](references/fresh-start.md)
- [Wrap Up](references/wrap-up.md)
- [Life Scan](references/life-audit.md)
- [Solopreneur Strategic Framework](references/solopreneur-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation with Wayve CLI shell commands and JSON-backed results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the wayve CLI, WAYVE_API_KEY, and user confirmation before creating automations or saving sensitive memories.]

## Skill Version(s):

1.0.13 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
