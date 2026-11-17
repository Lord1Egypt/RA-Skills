## Description:

Работа со СберБизнес API: онбординг со ссылками, Zero-Knowledge Vault (AES-256-GCM), ротация Client Secret (40 дней) и refresh-токенов, каналы уведомлений (Telegram/MAX/Discord/Slack/Webhook), остатки, лимиты тарифа, платёжки со ссылкой на подпись, PDF со штампом банка.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthet1x](https://clawhub.ai/user/synthet1x)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and finance operators use the skill to connect to SberBusiness, check balances and statements, configure transaction alerts, prepare payment drafts for signing, download bank documents, and manage API credentials.

### Deployment Geography for Use:

Russian Federation

## Known Risks and Mitigations:

Risk: The banking integration's credential handling and privacy controls fall short of its advertised protections.

Mitigation: Wait for fixes before connecting live banking credentials. Request protected credential transport, enforced memory-only temporary storage, validated download destinations, and reliable alert state handling.

Risk: Transaction alerts contain sensitive financial information, and masking does not protect custom webhook payloads.

Mitigation: Restrict notification recipients and use private channels; do not rely on masking to protect custom webhook payloads.

## Reference(s):

- [Human setup guide](references/HUMAN_GUIDE.md)
- [Notification channels guide](references/NOTIFICATION_CHANNELS.md)
- [SberBusiness online bank](https://sbi.sberbank.ru)

## Skill Output:

**Output Type(s):** [Banking API data, Shell commands, Configuration, PDF files, Guidance]

**Output Format:** [Text and JSON results, shell commands, configuration, and downloaded PDF statements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Banking data may include balances, transactions, counterparties, payment draft details, and account identifiers.]

## Skill Version(s):

1.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
