## Description:

Manages Kuaidaili proxy IP service credentials, order lookups, IP retrieval, expiry checks, health checks, concurrency recommendations, and usage statistics for agents working with Kuaidaili accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuaidaili-ai](https://clawhub.ai/user/kuaidaili-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users with Kuaidaili proxy accounts use this skill to configure local API credentials, retrieve proxy endpoints, inspect order state, monitor expiry and proxy health, and tune request concurrency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Kuaidaili API secrets locally in plaintext.

Mitigation: Use it only in a private environment, restrict permissions on the config file, avoid shared machines, and rotate credentials after testing.

Risk: Proxy credentials or usable proxy addresses may appear in output or logs.

Mitigation: Avoid pasting real secrets into shell commands or shared chats, review transcripts and logs, and remove or rotate exposed credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuaidaili-ai/skills/proxy-ip-manager)
- [Kuaidaili API response reference](references/api_response.md)
- [IP scoring and concurrency rules](references/scoring_rules.md)
- [Kuaidaili user center](https://www.kuaidaili.com/uc/overview/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, terminal text, and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked Kuaidaili API credentials, proxy connection strings, order status, expiry notifications, health scores, and concurrency recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
