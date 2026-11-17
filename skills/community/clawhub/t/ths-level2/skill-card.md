## Description:

同花顺Level2数据接入 helps agents read local TongHuaShun market-data artifacts, analyze stock quotes and Level2 signals, and generate technical analysis reports.

This skill is for research and development only.

## Publisher:

[claremouse007](https://clawhub.ai/user/claremouse007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance analysts use this skill to configure TongHuaShun and Tushare data access, run Python-based stock and Level2 analyses, and produce reports for review. It is best suited to authorized research or development workflows because the evidence describes reverse-engineered access, memory reading, and private protocol analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reverse-engineered market-data access may violate product terms or exceed the user's authorization.

Mitigation: Use only with explicit authorization and prefer official documented APIs or exported data when available.

Risk: Memory-reading scripts can inspect another application's process memory and may require elevated privileges.

Mitigation: Review the code before use and do not run memory-reading scripts as administrator.

Risk: Credential handling may expose a live Tushare token if stored in the skill directory.

Mitigation: Use environment variables or an external secret store instead of committing or storing tokens in the artifact.

Risk: Generated stock reports may be simulated, incomplete, or unsuitable as financial advice.

Mitigation: Treat outputs as research artifacts and require human review against authoritative market data before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claremouse007/skills/ths-level2)
- [Publisher profile](https://clawhub.ai/user/claremouse007)
- [Tushare documentation](https://tushare.pro/document/1)
- [TongHuaShun official website](https://www.10jqka.com.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with Python and shell snippets plus generated JSON and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on local TongHuaShun installation state, Tushare credentials, network access, and paid Level2 data authorization.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
