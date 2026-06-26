## Description: <br>
quotedance-market generates structured global market intelligence reports from market data and professional news sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoocky](https://clawhub.ai/user/yoocky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market-focused users and agents use this skill to generate trading-day or weekend market reports that combine global index, equity, futures, sector, and news signals. The reports are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated market reports may be mistaken for investment advice. <br>
Mitigation: Treat reports as informational, verify underlying data independently, and apply human review before making financial decisions. <br>
Risk: The skill contacts financial and news services, may use a configured proxy, and can fall back to curl for network requests. <br>
Mitigation: Review network configuration, proxy settings, and any Quotedance API key before running in a controlled environment. <br>
Risk: The skill keeps local market snapshots and news cache files. <br>
Mitigation: Review and clear the memory directory as needed, and avoid placing secrets or sensitive portfolio data in cached outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoocky/quotedance-market) <br>
- [Quotedance service endpoint](https://quotedance.api.gapgap.cc) <br>
- [Yahoo Finance quote endpoint](https://query1.finance.yahoo.com/v7/finance/quote) <br>
- [Bloomberg markets RSS](https://feeds.bloomberg.com/markets/news.rss) <br>
- [Reuters business news RSS](https://feeds.reuters.com/reuters/businessNews) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown market report with console logs and local JSON snapshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports --refresh and --net-debug; may write market snapshots and news cache files under the skill memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
