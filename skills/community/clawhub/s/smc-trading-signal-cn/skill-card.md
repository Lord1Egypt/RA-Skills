## Description:

Generates Smart Money Concepts trading-signal summaries using 1H trend direction, 15M entry cues, and ATR-based stop-loss and take-profit levels, with the current implementation focused on gold market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt6558609-cpu](https://clawhub.ai/user/zt6558609-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to monitor configured market symbols and produce reference trading-signal summaries with entry, stop-loss, take-profit, and risk notes. The outputs should not be treated as production financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals may be generated from unverified or simulated market data.

Mitigation: Verify market prices independently before acting, and disable mock or fallback data for any real trading workflow.

Risk: The skill may overstate market coverage and currently focuses on gold data despite broader market claims.

Mitigation: Treat non-gold symbols as unsupported until their data feeds and signal logic are validated.

Risk: Generated outputs may be mistaken for financial advice.

Mitigation: Use the signals only as reference material and apply independent review, position sizing, and stop-loss controls before any trade.

Risk: One market-data request in the artifact disables TLS certificate verification.

Mitigation: Use a trusted data source with certificate verification enabled before scheduling or relying on the monitor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zt6558609-cpu/skills/smc-trading-signal-cn)
- [Project repository listed by artifact](https://github.com/zt6558609-cpu/smc-trading-signal)
- [Sina Finance COMEX gold endpoint used by artifact](https://hq.sinajs.cn/list=hf_GC)
- [Yahoo Finance COMEX gold chart endpoint used by artifact](https://query1.finance.yahoo.com/v8/finance/chart/GC=F)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown signal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write signal_*.md files under scripts/output when a signal is found.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
