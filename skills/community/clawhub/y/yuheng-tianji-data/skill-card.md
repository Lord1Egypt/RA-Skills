## Description:

Tianji Data helps agents collect and format free real-time Chinese A-share, Hong Kong index, QDII ETF, commodity, policy, and macro-market signals for market monitoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizoncove](https://clawhub.ai/user/horizoncove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to gather real-time and near-real-time Chinese market data, normalize snapshots, and prepare alert-oriented financial context. It is suited for data collection and monitoring support, not for unattended trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports under-disclosed alerting behavior that can send messages to a fixed Feishu user and uses an unsafe subprocess pattern.

Mitigation: Review or remove market_watcher.py notification behavior before installation; replace python3 -c interpolation with a direct safe API call and require explicit opt-in for outbound alerts.

Risk: The artifact writes alert records and state to local workspace and temporary paths.

Mitigation: Document exact write paths, store state in a private application directory, and define cleanup rules before deployment.

Risk: Market data and alert outputs can be stale, unavailable, or misleading if source endpoints fail or return abnormal values.

Mitigation: Keep the documented freshness checks, cross-source validation, null handling, and anomaly review before using outputs for decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/horizoncove/skills/yuheng-tianji-data)
- [Free Data Sources](artifact/references/free-data-sources.md)
- [Tencent quote endpoint examples](https://qt.gtimg.cn/q=hkHSI)
- [Sina commodity endpoint example](https://hq.sinajs.cn/list=hf_GC)
- [Eastmoney Shanghai Composite quote page](https://quote.eastmoney.com/zs000001.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples, JSON data schemas, and formatted market snapshot text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or describe JSON market snapshots, alert queue records, and formatted console output; runtime scripts perform outbound market-data requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
