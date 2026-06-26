## Description: <br>
Guides OpenClaw agents through Yandex Metrika API reporting, Logs API workflows, management tasks, OAuth setup, presets, UTM analysis, CSV export, and quota handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horosheff](https://clawhub.ai/user/horosheff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analytics operators use this skill to connect OpenClaw to Yandex Metrika, choose the right API endpoint, produce reports or export commands, and handle OAuth tokens, counters, logs, imports, and quota issues safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users toward broad Yandex Metrika OAuth access. <br>
Mitigation: Use a user-owned Yandex OAuth app, prefer metrika:read for reporting, and add write or import scopes only for tasks that require changes. <br>
Risk: OAuth tokens could be exposed in chat, files, logs, or support channels. <br>
Mitigation: Store tokens only in OpenClaw secrets or environment variables, use placeholders in commands, and never send tokens or passwords through Telegram or private messages. <br>
Risk: Management, import, access-grant, and log-cleanup operations can change or remove account data. <br>
Mitigation: Require explicit user confirmation before POST, PUT, DELETE, access grant, import, or log cleanup operations. <br>
Risk: Reports can hit API quotas or include privacy-restricted data. <br>
Mitigation: Handle 429 responses as quota events and check contains_sensitive_data before presenting report details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horosheff/yandex-metrika-assistant) <br>
- [Project homepage](https://github.com/Horosheff/yandex-metrika-assistant) <br>
- [Yandex Metrika API hub](https://yandex.ru/dev/metrika) <br>
- [Yandex Metrika Stat API](https://yandex.ru/dev/metrika/ru/stat/) <br>
- [Yandex OAuth overview](https://yandex.ru/dev/id/doc/ru/concepts/ya-oauth-intro) <br>
- [Bundled user intents matrix](docs/10-user-intents-matrix.md) <br>
- [Bundled OAuth token instructions](docs/INSTRUCTION-GET-TOKEN-RU.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with PowerShell and curl command examples, API parameter templates, and concise report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OAuth tokens from OpenClaw secrets or environment variables and avoids echoing token values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
