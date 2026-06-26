## Description: <br>
每日科技资讯聚合。自动抓取GitHub Trending、51CTO、百度热搜科技榜，筛选AI/Cloud/ML领域内容，生成结构化简报。触发词：科技日报、tech news、每日资讯、科技资讯 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgugeng](https://clawhub.ai/user/lgugeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation operators use this skill to collect technology and AI news, filter items by configured topics, generate daily briefings, and optionally deliver them to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports that claimed source coverage and verification do not match the code or bundled outputs. <br>
Mitigation: Treat generated briefings as unverified until the source and filtering behavior is reviewed and corrected. <br>
Risk: The artifact includes scheduled execution paths for daily runs. <br>
Mitigation: Disable or remove the cron configuration unless unattended daily fetching is intended. <br>
Risk: The artifact includes external delivery paths and a configured push target. <br>
Mitigation: Configure any Feishu webhook yourself and remove or replace the bundled push target before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lgugeng/tech-news-daily-lgugeng) <br>
- [Publisher profile](https://clawhub.ai/user/lgugeng) <br>
- [GitHub Trending API](https://api.github.com/search/repositories) <br>
- [Baidu technology hot list](https://top.baidu.com/board?tab=realtime&category=tech) <br>
- [Feishu webhook configuration](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, JSON report files, Feishu card payloads, and shell or Python execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local report/state files under data/ and briefings/; Feishu delivery requires user-supplied webhook configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
