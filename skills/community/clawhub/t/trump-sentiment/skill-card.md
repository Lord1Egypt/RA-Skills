## Description: <br>
Monitors Trump-related posts, news, and market reactions across Truth Social, Google News, X search, and selected market accounts to produce concise sentiment analysis for investment decision support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors and market analysts use this skill to collect Trump-related political and geopolitical signals, compare them with market reactions, and produce a time-ordered sentiment report for decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated political and market monitoring can produce incomplete, stale, or misleading interpretations. <br>
Mitigation: Require human review of sources, timestamps, and market context before acting on any generated analysis. <br>
Risk: The skill may deliver reports to external Feishu channels. <br>
Mitigation: Review and limit outbound report delivery settings before use, especially for sensitive market commentary. <br>
Risk: Permission metadata includes wallet, purchase, credential, and crypto-related capabilities that may not match normal sentiment reporting needs. <br>
Mitigation: Disable high-impact permissions unless they are explicitly required and verified for the deployment. <br>
Risk: Generated investment implications are commentary, not financial advice. <br>
Mitigation: Treat outputs as unverified decision-support material and validate them against primary sources and internal risk controls. <br>


## Reference(s): <br>
- [Trump Sentiment skill page](https://clawhub.ai/gold3bear/trump-sentiment) <br>
- [Truth Social @realDonaldTrump](https://truthsocial.com/@realDonaldTrump) <br>
- [Google News Trump Iran one-hour search](https://news.google.com/search?q=Trump+Iran&when=1h) <br>
- [Google News RSS Trump Iran ceasefire one-hour search](https://news.google.com/rss/search?q=Trump+Iran+ceasefire+when:1h&hl=en-US&gl=US&ceid=US:en) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown sentiment report with source timeline, market reaction notes, contradiction flags, and investment implications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include timestamps, source labels, engagement counts, market prices, and Feishu delivery identifiers when report delivery is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
