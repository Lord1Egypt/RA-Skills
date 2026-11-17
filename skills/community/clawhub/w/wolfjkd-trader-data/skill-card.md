## Description:

Provides A-share market data guidance and a Python router that probes Tencent, Wind, and ftshare sources, scores their health, and selects a source for quotes, watchlists, announcements, and comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolfjkd](https://clawhub.ai/user/wolfjkd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance-focused agent builders use this skill to set up A-share market data access, configure optional Wind and ftshare sources, and route quote, watchlist, announcement, or source-comparison requests through available data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags unsafe, mutable dependency installation paths in setup guidance.

Mitigation: Review and pin third-party skills and Python packages before installation, and avoid untrusted or mutable install sources.

Risk: The setup guidance includes an HTTP pip mirror command.

Mitigation: Use HTTPS package indexes or trusted internal mirrors, and avoid the documented HTTP mirror command.

Risk: Optional Wind setup can broaden API-key exposure when configured globally.

Mitigation: Use an isolated environment and credentials scoped only to the market-data access required for the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wolfjkd/skills/wolfjkd-trader-data)
- [Publisher profile](https://clawhub.ai/user/wolfjkd)
- [Skill deployment guide](artifact/SKILL.md)
- [Project README](artifact/README.md)
- [Data router source](artifact/data_router.py)
- [Tencent quote endpoint](https://qt.gtimg.cn/)
- [Wind financial data service](https://www.wind.com.cn/)
- [AkShare documentation](https://akshare.akfamily.xyz/)
- [Wind skills repository](https://gitee.com/wind_info/wind-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and CLI examples; the router can emit terminal tables or JSON for quote and watchlist commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The router may call external market-data services and optional local skills; users should label data sources and scores in downstream reports.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
