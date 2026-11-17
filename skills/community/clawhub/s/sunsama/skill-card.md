## Description:

Helps agents manage Sunsama tasks, daily plans, calendars, timers, and connected email threads through a user's authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Sunsama users and their assistants use this skill to find and organize tasks, plan calendar time, track work, and handle email threads in connected accounts. It also describes optional user-approved automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected Sunsama and email or calendar accounts may expose personal information or allow changes to user data.

Mitigation: Review connection scopes, use least privilege, confirm the intended account and target, and obtain explicit approval before writes or deletes.

Risk: Persistent functions, triggers, or destinations can keep acting on events or forward data after a one-time request.

Mitigation: Require separate, explicit approval for each automation and destination; review its scope and recipients, and remove it when no longer needed.

Risk: Using or exposing long-lived API keys can compromise connected accounts.

Mitigation: Prefer the CLI OAuth login; do not display, log, or embed credentials, and rotate any exposed key.

## Reference(s):

- [Sunsama skill release](https://clawhub.ai/byungkyu/skills/sunsama)
- [Maton](https://maton.ai)
- [Maton API Reference](https://docs.maton.ai/api-reference/overview)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Sunsama](https://sunsama.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with commands and structured API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain personal task, calendar, or email information from authorized connections.]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
