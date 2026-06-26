## Description: <br>
美股IPO机会扫描 helps agents monitor public IPO, new listing, fund, social, and market-news signals to identify early U.S. stock opportunity leads for further user review. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[aidalong](https://clawhub.ai/user/aidalong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, researchers, and market-monitoring agents use this skill to scan public IPO feeds, social feeds, and financial-news sources for early leads. The resulting signals are intended for further research, not automated investment or trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public market, social, and news signals may be incomplete, stale, or unverified. <br>
Mitigation: Treat outputs as leads for additional research and verify signals against authoritative market sources before acting. <br>
Risk: IPO and thematic-stock signals could be mistaken for investment advice. <br>
Mitigation: Keep recommendations framed as research prompts and do not use the skill to make automated investment or trading decisions. <br>
Risk: Automated alerts can amplify noisy or speculative social-media activity. <br>
Mitigation: Keep alerts user-configured, tune keyword thresholds, and review high-priority signals manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aidalong/us-stock-ipo-scanner) <br>
- [Detailed signal source list](artifact/references/sources.md) <br>
- [Invezz IPO feed](https://invezz.com/news/stocks/ipos/feed/) <br>
- [Nasdaq IPO calendar](https://www.nasdaq.com/market-activity/ipos) <br>
- [CNBC IPO news RSS](https://www.cnbc.com/id/100003114/device/rss/rss.html) <br>
- [Seeking Alpha IPO market news](https://seekingalpha.com/market-news/ipos.xml) <br>
- [Benzinga market news feed](https://www.benzinga.com/feed) <br>
- [RSS.app](https://rss.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown scanning report with source links, signal layers, keywords, and research recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market, news, and social feeds; alerts and keyword rules should remain user-configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
