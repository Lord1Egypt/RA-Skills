## Description:

xtdata helps agents use XtQuant and miniQMT market-data APIs for real-time quotes, K-line bars, Tick, Level2, financial, instrument, and sector data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative-analysis agents use this skill to retrieve, subscribe to, and reason over XtQuant market data from a local QMT or miniQMT environment. It is useful for building data-download, quote-monitoring, financial-data, Level2-analysis, and sector/instrument lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes trading, cancellation, transfer, export, import, and sector deletion/reset documentation alongside market-data guidance.

Mitigation: Use isolated accounts and environments, and require explicit human confirmation before any order, cancellation, transfer, export, import, or destructive sector-management action.

Risk: Sample account, bank-account, and password values appear in trading and transfer examples.

Mitigation: Never reuse sample credentials or account identifiers; route secrets through approved secret-management controls.

Risk: Market-data outputs can be stale, incomplete, permission-limited, or unavailable when QMT/miniQMT is not running or the broker does not provide the requested feed.

Mitigation: Check connection state, permissions, timestamps, empty results, and missing values before using returned data in analysis or downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderwpf/skills/xtdata)
- [ClawHub publisher profile](https://clawhub.ai/user/coderwpf)
- [XtData documentation](http://dict.thinktrader.net/nativeApi/xtdata.html)
- [XtQuant getting started](http://dict.thinktrader.net/nativeApi/start_now.html)
- [BossQuant Bilibili support page](https://space.bilibili.com/48693330)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes a Python environment with xtquant, pandas, and a local QMT or miniQMT client.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
