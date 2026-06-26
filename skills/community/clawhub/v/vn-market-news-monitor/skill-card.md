## Description: <br>
Tracks Vietnam market and sector narratives from major domestic financial media; used when users ask for market stories, sector heat, and most-mentioned Vietnamese tickers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to monitor Vietnamese financial media for current market narratives, sector intensity, ticker mentions, and narrative shifts. It supports signal monitoring only, not buy or sell recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Limited or stale source coverage can distort market narrative rankings. <br>
Mitigation: Report the collection window, last update per source, source coverage table, and downgrade confidence when fewer than three domestic sources are available. <br>
Risk: Headline noise, duplicate coverage, or one-source concentration can overstate a sector or ticker narrative. <br>
Mitigation: Deduplicate by normalized title and publisher domain, flag concentration above 50 percent from one source, and label major claims as Fact or Inference. <br>
Risk: Users could mistake media-monitoring signals for investment advice. <br>
Mitigation: Do not issue buy or sell commands; present outputs as monitoring signals and recommend cross-checking with quantitative metrics before investment action. <br>


## Reference(s): <br>
- [CafeF](https://cafef.vn/) <br>
- [VnEconomy](https://vneconomy.vn/) <br>
- [VietnamFinance](https://vietnamfinance.vn/) <br>
- [Vietstock](https://vietstock.vn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with source coverage, freshness, sector intensity, ticker mentions, narrative shifts, risks, and validation checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confidence labels, source links for major statements, Fact versus Inference tags, and optional watchlist impact mapping.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
