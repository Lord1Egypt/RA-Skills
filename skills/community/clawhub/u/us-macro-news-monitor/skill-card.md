## Description: <br>
Tracks US macro signals from Bloomberg, WSJ, and Reuters and maps potential spillover to Vietnam sectors; used when users ask about US macro news and likely impacts on Vietnamese equities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to monitor recent US macroeconomic news, classify themes and tone, and map likely spillover channels to Vietnam sectors and watchlist tickers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial news coverage may be incomplete, stale, blocked, or paywalled. <br>
Mitigation: Use the skill's freshness window, source-count threshold, missingness log, official-source fallbacks, and confidence downgrade rules before relying on results. <br>
Risk: Vietnam sector and ticker impacts are inferred research signals, not personalized investment advice. <br>
Mitigation: Label claims as Fact or Inference, avoid absolute buy/sell instructions, and verify cited financial news independently. <br>
Risk: Macro narratives can be over-attributed to sector moves when source confirmation is weak. <br>
Mitigation: Cross-check distinct sources, report the main uncertainty driver, and treat low-source or concentrated coverage as Low confidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ndtchan/us-macro-news-monitor) <br>
- [Bloomberg](https://www.bloomberg.com/) <br>
- [Wall Street Journal](https://www.wsj.com/) <br>
- [Reuters Markets](https://www.reuters.com/markets/) <br>
- [Federal Reserve](https://www.federalreserve.gov/) <br>
- [Bureau of Labor Statistics](https://www.bls.gov/) <br>
- [Bureau of Economic Analysis](https://www.bea.gov/) <br>
- [FRED](https://fred.stlouisfed.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown sections with source URLs, theme counts, tone distribution, Vietnam sector spillover map, watchlist items, and confidence notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current web/news access; confidence depends on source availability, freshness, paywall coverage, and cross-confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
