## Description:

Trading_Agents_for_Futures analyzes futures markets across technical, basis, term structure, inventory, positioning, and news dimensions, returning structured JSON metrics and optional debate-style risk decision reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoge10241024](https://clawhub.ai/user/haoge10241024)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading analysts use this skill to collect public futures-market signals, identify data gaps for agent-assisted follow-up, and generate structured indicators or decision-support reports. Outputs should be independently checked and not treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may modify the active Python environment.

Mitigation: Install and run the skill in a virtual environment, avoid administrator/root execution, and review or pin dependencies before use.

Risk: Market-data downloads, caches, and output files may contain stale, incomplete, or locally sensitive analysis artifacts.

Mitigation: Verify data freshness independently and protect cache, output, and log locations according to the user's data-handling requirements.

Risk: Decision-mode outputs can be mistaken for investment advice.

Mitigation: Treat buy, sell, position, and risk outputs as decision-support material only and validate suitability with independent market and risk review.

Risk: Proxy credentials or other sensitive configuration values could be exposed if placed in configuration or logs.

Mitigation: Avoid storing credentials in config files for this skill; if proxy settings are required, protect logs and configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haoge10241024/skills/trading-agents-for-futures)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Skill manifest](artifact/manifest.yaml)

## Skill Output:

**Output Type(s):** [json, markdown, text, guidance]

**Output Format:** [Structured JSON with optional Markdown-like decision reports and search-action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coverage, warning_flags, data_gap_report, and ai_fill slots for missing market data.]

## Skill Version(s):

2.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
