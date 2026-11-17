## Description:

基于100个热门TradingView Pine Script指标转换的Python技术分析工具集，提供专业的技术指标计算、分析和可视化功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[super-max21](https://clawhub.ai/user/super-max21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to request TradingView-style technical-indicator analysis, calculations, visualization support, and related implementation guidance through a Prana-hosted skill wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and related market-analysis content are sent to the Prana remote service.

Mitigation: Use a trusted HTTPS Prana endpoint and avoid sending sensitive or confidential market data unless the deployment has approval for that data flow.

Risk: API credentials can be persisted in plaintext configuration files.

Mitigation: Prefer scoped PRANA_* environment variables, restrict local file permissions, and keep credential files out of source control, backups, and shared archives.

Risk: The Prana base URL can be overridden by environment configuration.

Mitigation: Set NEXT_PUBLIC_URL only to a trusted HTTPS endpoint and avoid running the skill in untrusted environments that can alter runtime variables.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/super-max21/skills/zyz-skill-100-indicators-analysis-public)
- [Publisher profile](https://clawhub.ai/user/super-max21)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable analysis or implementation guidance, returned through the configured agent channel or JSON client response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain a thread_id for multi-turn use; responses depend on the remote Prana skill and user-provided market-analysis prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
