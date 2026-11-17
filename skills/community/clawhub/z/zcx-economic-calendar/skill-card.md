## Description:

Track and analyze global economic data releases, central bank meetings, and key financial events across major economies with impact ratings, market expectations, and trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-focused analysts use this skill to assemble daily or weekly economic calendars, compare expected and prior releases, and summarize likely market impact around macroeconomic and central-bank events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make disclosed network requests to external government data sites when gathering economic data.

Mitigation: Install and run it only where those outbound requests are acceptable, and review the referenced data URLs before use.

Risk: Market data, expectations, and trading implications may be incomplete, stale, or unsuitable for a specific decision.

Mitigation: Verify economic data and trading implications independently before acting on them.

## Reference(s):

- [China National Bureau of Statistics data query](https://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgnd&rowcode=zb&colcode=sj&wds=[]&dfwds=[])
- [Federal Reserve Data Download](https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&series=bcb44e57fb57efbe90002369321bfb3f&lastobs=&from=&to=&filetype=csv)
- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/zcx-economic-calendar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown calendar summaries, market-impact tables, trading guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference disclosed external government data sources through curl examples.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
