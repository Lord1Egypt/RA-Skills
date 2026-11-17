## Description:

中国体育彩票全玩法号码分析、条件筛选、走势图、历史数据查询与数据参考综合工具。

This skill is for research and development only.

## Publisher:

[xljcheng](https://clawhub.ai/user/xljcheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to analyze China Sports Lottery CSV data, generate statistical reports, validate numbers, compute combinations, and produce non-predictive reference outputs. It is framed for data analysis and learning, not betting advice or gambling execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unsafe installation guidance using a remote shell installer.

Mitigation: Review installation steps before use and avoid running curl-piped shell commands unless the installer source is independently trusted and verified.

Risk: Some scripts fetch lottery data from external websites and cache or process local CSV files.

Mitigation: Use trusted CSV inputs, review fetched data before relying on it, and treat external data sources as untrusted until validated.

Risk: The skill produces betting-adjacent statistics, generated number sets, probability calculations, and winner checks.

Mitigation: Present outputs as non-predictive analysis only, avoid betting recommendations, and remind users that lottery outcomes are random.

Risk: The artifact contains inconsistent statements about network fetching and data freshness.

Mitigation: Tell users whether data came from a provided CSV, local cache, generated sample data, or an online fetch before interpreting results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xljcheng/skills/ticai-game-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/xljcheng)
- [500.com historical lottery API](https://ews.500.com/xcxkj/kaijiang/history)
- [500star historical lottery charts](https://datachart.500star.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown or terminal text with optional CSV and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be treated as statistical reference material and not as predictions or betting recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
