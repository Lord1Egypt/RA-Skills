## Description: <br>
Tech Radar Daily scans GitHub Trending, Product Hunt, Hacker News, and Awesome Lists to identify, score, de-duplicate, archive, and send a daily digest of selected technology intelligence to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dereklu515](https://clawhub.ai/user/dereklu515) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and technical operators use this skill to monitor public technology sources and receive a daily Feishu digest of notable tools, trends, and monetizable projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security evidence flags an under-documented Feishu chat-listing helper that can use Feishu app credentials to read organization chat metadata. <br>
Mitigation: Review or remove scripts/test-feishu-chat.js unless chat listing is intended, and only provide Feishu app credentials with the minimum required permissions. <br>
Risk: Normal runs fetch public technology sources, save local cache/report/log files, and can send the generated digest to a configured Feishu webhook. <br>
Mitigation: Use a dedicated Feishu webhook, review digest contents before broad distribution, and understand what local data the skill writes before scheduling it. <br>
Risk: The skill can use a GitHub token and proxy settings during collection. <br>
Mitigation: Use a least-privilege GitHub token, configure only trusted proxies, and keep environment variables out of committed files and shared logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dereklu515/tech-radar-daily) <br>
- [Awesome Lists source catalog](references/awesome-lists.md) <br>
- [Search query catalog](references/search-queries.md) <br>
- [GitHub Trending daily source](https://github.com/trending?since=daily) <br>
- [Product Hunt source](https://www.producthunt.com) <br>
- [Hacker News API source](https://hacker-news.firebaseio.com/v0/topstories.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, API Calls] <br>
**Output Format:** [Markdown daily digest and Feishu text message, with JSON cache and stats files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces up to 7-9 selected items in normal runs; Feishu delivery requires FEISHU_WEBHOOK_URL.] <br>

## Skill Version(s): <br>
1.0.9 (source: evidence release, target metadata, and SKILL.md frontmatter; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
