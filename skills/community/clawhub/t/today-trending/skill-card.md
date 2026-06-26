## Description: <br>
获取今日微博、抖音、百度热搜排行榜，帮助用户一站式查询实时热门话题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[php737](https://clawhub.ai/user/php737) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current trending-topic lists from Weibo, Douyin, and Baidu, then summarize or analyze those topics for a quick view of public online trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Weibo, Douyin, and Baidu when invoked and depends on their public pages or API responses. <br>
Mitigation: Run it only where those outbound requests are permitted, and treat empty or failed platform results as expected behavior when upstream responses change or are unavailable. <br>
Risk: The returned topics are volatile third-party public content and may be incomplete, sensitive, or unsuitable for direct user-facing decisions. <br>
Mitigation: Review and contextualize results before summarizing them or using them in downstream decisions. <br>
Risk: Runtime behavior depends on Python packages such as requests and lxml. <br>
Mitigation: Verify and install required Python dependencies in the execution environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/php737/today-trending) <br>
- [Publisher profile](https://clawhub.ai/user/php737) <br>
- [Weibo hot search](https://weibo.com/hot/search) <br>
- [Baidu realtime trends](https://top.baidu.com/board?tab=realtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object printed to standard output, with platform names mapped to ranked topic-title lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill accepts a JSON request containing a platform value of weibo, douyin, baidu, or all.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
