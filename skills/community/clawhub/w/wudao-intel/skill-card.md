## Description: <br>
Provides A-share market intelligence for dragon-tiger board activity, research reports, auction data, AI-curated hot lists, daily briefings, and notable trading seats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdreamjc](https://clawhub.ai/user/jcdreamjc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer A-share market intelligence questions about hot topics, research reports, analyst ratings, pre-market auction data, daily briefings, and dragon-tiger board activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided API key for the stock.quicktiny.cn market-data API. <br>
Mitigation: Keep LB_API_BASE pointed at the expected provider URL, protect LB_API_KEY, and rotate the key as needed. <br>
Risk: Returned market analysis and briefings may be incomplete, stale, or unsuitable as financial advice. <br>
Mitigation: Treat results as informational market intelligence and review them independently before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcdreamjc/wudao-intel) <br>
- [悟道 market-data service](https://stock.quicktiny.cn) <br>
- [OpenClaw API base](https://stock.quicktiny.cn/api/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
