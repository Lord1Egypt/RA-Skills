## Description:

Provides agent-accessible market data tools for A-share, Hong Kong, U.S., fund, futures, options, bond, index, macro, financial, and news workflows through StockToday backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usa2046](https://clawhub.ai/user/usa2046)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and agent users use this skill to retrieve market quotes, financial statements, indexes, funds, futures, macro indicators, announcements, and news, then convert the data into concise summaries, tables, exports, or reusable scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts StockToday backend services using a user-provided API token.

Mitigation: Install only where that backend access is acceptable, keep the token in protected environment or MCP configuration, and rotate the token if it is exposed.

Risk: The security evidence flags unpinned npx install or update commands and an automatic npx version check.

Mitigation: Pin versions and review the publisher release before installing or updating in sensitive environments.

Risk: The security guidance identifies plaintext HTTP fallback endpoints as a transport concern.

Mitigation: Prefer HTTPS-only backend configuration and avoid plaintext fallback endpoints unless the deployment environment explicitly accepts that risk.

Risk: The skill writes a local token-status cache.

Mitigation: Run it under a trusted user account, keep local profile permissions restricted, and clear the cache on shared machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/usa2046/skills/stocktoday-skill)
- [StockToday token site](https://stocktoday.cn)
- [Interface documentation](https://github.com/stocktoday/stocktoday-skill/blob/main/INTERFACE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown summaries, compact tables, JSON tool results, CSV or Parquet exports, and Python scripts when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data scope, source, units, time window, caveats, and file paths when local exports are produced.]

## Skill Version(s):

1.3.11 (source: server release evidence, package.json, _meta.json, RELEASE_NOTES.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
