## Description:

三立期货「三立智期」官方技能：对话领取模拟盘密钥，查行情与持仓，模拟盘可下单；问是否正规、开户也可答。实盘请去 App 复制密钥。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqringwang](https://clawhub.ai/user/sqringwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Sanli Zhiqi futures services for simulated trading setup, market data, account and position review, and supported order workflows. Live trading use depends on a user-provided app-issued key and should be reviewed before any order action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access trading account data and submit or cancel orders when configured.

Mitigation: Install only if the publisher is trusted, keep the environment on sim unless live trading is intentional, and review live order details before approval.

Risk: Stored API key files are sensitive secrets.

Mitigation: Treat credential files as sensitive, avoid sharing full keys, and keep file permissions restricted.

Risk: Endpoint configuration mistakes could direct requests to an unintended service.

Mitigation: Use the official HTTPS API domain and avoid configuring non-HTTPS or non-official domains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sqringwang/skills/slzq-trading-preview)
- [Sanli Futures official website](https://www.sxslqh.com/)
- [Usage notes](references/usage-notes.md)
- [Company FAQ](references/company-faq.md)
- [Open API index](references/api.md)
- [OpenAPI contract](references/openapi.yaml)
- [MCP runtime README](runtime/mcp/README.md)
- [OpenClaw API domain](https://slzqapi.sxslqhsh.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and structured API/tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May handle trading credentials, simulated-order actions, and live-order authority when configured by the user.]

## Skill Version(s):

1.2.8 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
