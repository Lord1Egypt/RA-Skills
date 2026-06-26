## Description: <br>
Cross-reference restaurant recommendations from Xiaohongshu (小红书) and Dianping (大众点评) to validate restaurant quality and consistency. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[liyang2016](https://clawhub.ai/user/liyang2016) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to compare restaurant signals from Dianping and Xiaohongshu for a city or district, then rank candidates by cross-platform consistency, review volume, engagement, and sentiment. It is most appropriate for research or personal decision support where the user can review low-confidence matches and platform discrepancies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable local login sessions for third-party platforms. <br>
Mitigation: Treat the sessions directory and any ClawHub token as secrets, keep them local, and reset sessions when access is no longer needed. <br>
Risk: Some recommendation paths may return simulated data while being presented as validation. <br>
Mitigation: Confirm whether a result came from the real browser-backed workflow before using it for decisions, and label mock or server-mode output as test data. <br>
Risk: The skill depends on scraping Dianping and Xiaohongshu, which may conflict with platform terms or account expectations. <br>
Mitigation: Review platform terms and account risk before use, prefer official APIs or permitted data providers for commercial use, and apply conservative rate limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liyang2016/restaurant-crosscheck) <br>
- [Data schema documentation](references/data_schema.md) <br>
- [Sentiment analysis guide](references/sentiment_analysis.md) <br>
- [API limitations](references/api_limitations.md) <br>
- [Dianping](https://www.dianping.com) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style restaurant recommendation summaries with scores, platform comparisons, warnings, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendation scores use a 0-10 scale and consistency levels identify high, medium, and low confidence matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
