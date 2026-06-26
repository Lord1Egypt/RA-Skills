## Description: <br>
获取实时微博热搜榜单，按热度排序，无需 API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenzihao0731](https://clawhub.ai/user/chenzihao0731) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch current Weibo trending topics for China-focused news, social media monitoring, or command-line integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each use contacts the disclosed v2.xxapi.cn third-party service for public Weibo trend data. <br>
Mitigation: Deploy only where that network call is acceptable, and cache or throttle requests when frequent polling is expected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenzihao0731/weibo-hot) <br>
- [Publisher profile](https://clawhub.ai/user/chenzihao0731) <br>
- [API homepage](https://v2.xxapi.cn) <br>
- [Weibo hot topics API](https://v2.xxapi.cn/api/weibohot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Line-oriented text in hotness|title format, with errors written to stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; no API key is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
