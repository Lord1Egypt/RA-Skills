## Description:

Guides OpenClaw agents through Yandex Metrika API reporting, Logs API export, management operations, OAuth setup, presets, UTM analysis, goals, CSV output, quotas, and safe token handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horosheff](https://clawhub.ai/user/horosheff)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to connect Yandex Metrika via OAuth, choose counters, compose API requests, interpret analytics responses, and troubleshoot quota or permission issues. It supports marketing analytics workflows such as traffic summaries, page performance, goals, CSV exports, raw logs, and data imports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request powerful Yandex OAuth access for reporting, management, and import workflows.

Mitigation: Use a user-owned Yandex OAuth application and grant only the scopes needed for the task, preferably read-only unless management or imports are required.

Risk: OAuth tokens, authorization codes, passwords, or screenshots containing credentials could be exposed through chat or third-party support channels.

Mitigation: Store secrets only in OpenClaw secrets, a secret manager, or local environment variables, and never send tokens to Telegram or any person.

Risk: Copied documentation examples may include full-looking OAuth token values or unsafe token handling patterns.

Mitigation: Replace any full-looking token example with a placeholder before reuse and rotate credentials if a real token was shared or logged.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/horosheff/skills/yandex-metrika-assistant)
- [Project Homepage](https://github.com/Horosheff/yandex-metrika-assistant)
- [Yandex Metrika API Hub](https://yandex.ru/dev/metrika)
- [Yandex Metrika Reports API](https://yandex.ru/dev/metrika/ru/stat/)
- [Yandex Metrika Management API](https://yandex.ru/dev/metrika/ru/management/)
- [Yandex Metrika Logs API](https://yandex.ru/dev/metrika/ru/logs/)
- [Yandex OAuth Documentation](https://yandex.ru/dev/id/doc/ru/concepts/ya-oauth-intro)
- [Yandex Metrika Quotas](https://yandex.ru/dev/metrika/ru/intro/quotas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API Calls]

**Output Format:** [Markdown responses with API request examples, command snippets, tables, and concise analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON or CSV request patterns and should avoid exposing OAuth tokens in generated output.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
