## Description: <br>
Stock Top Gainers retrieves the top 20 A-share stocks by gains over the most recent 10 trading days and filters out ST-designated stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to request a recent A-share stock gainers ranking, excluding ST-designated stocks. The output is informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return stale cached market data if live browsing fails. <br>
Mitigation: Check whether output came from live browsing or the dated cached sample before relying on it. <br>
Risk: Stock rankings may be misused as investment advice. <br>
Mitigation: Treat the output as informational market data and apply independent financial review before acting. <br>
Risk: Live retrieval uses browser access to public stock-data sites. <br>
Mitigation: Install and run the skill only in environments where this browser access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinelp100/stock-top-gainers) <br>
- [Publisher profile](https://clawhub.ai/user/shinelp100) <br>
- [Tonghuashun iWencai gainers query](https://www.iwencai.com/unifiedwap/result?w=%E8%BF%91%2010%20%E6%97%A5%E6%B6%A8%E5%B9%85%E6%8E%92%E5%90%8D) <br>
- [Eastmoney margin trading data](https://data.eastmoney.com/rzrq/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown table or JSON records containing ranked stock gainers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks up to 20 non-ST A-share stocks by 10-trading-day gain; live browser results may fall back to a dated cached sample.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, _meta.json, package.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
