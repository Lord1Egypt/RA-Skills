## Description:

Generate automated daily market reports for Chinese futures markets. Summarize sector performance, top movers, volume/OI changes, and produce formatted end-of-day summaries for distribution or PDF conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to assemble Chinese futures end-of-day market reports covering sector performance, top movers, volume, open interest, anomalies, and next-session watch items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF export of untrusted Markdown can expose local files or unsafe network access through renderer behavior.

Mitigation: Convert only trusted report Markdown and run PDF rendering in a sandboxed environment with limited file and network access.

Risk: Market summaries depend on live quote data and previous-day comparison data, so stale or missing inputs can produce incomplete or misleading reports.

Mitigation: Verify quote timestamps and mark open-interest changes as N/A when previous-day data is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/zcx-daily-market-report)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina Finance futures quote endpoint](https://hq.sinajs.cn/list=IF0,IC0,IH0,IM0,CU0,AL0,AU0,AG0,I0,RB0,HC0,SC0,LU0,MA0,TA0,SA0,EG0,C0,M0,Y0,P0,SR0,CF0,EC0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown daily market report with optional PDF conversion commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include calculated sector averages, gainers and losers, anomalies, volume/open-interest summaries, and PDF export guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
