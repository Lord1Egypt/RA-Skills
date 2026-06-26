## Description: <br>
小红书账号榜单追踪分析工具，支持查询日榜周榜月榜TOP50排名和热门账号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brands, MCN teams, and industry analysts use this skill to query Xiaohongshu daily, weekly, and monthly TOP 50 account rankings, filter by niche, generate visual HTML reports, and optionally subscribe to recurring ranking updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires REDFOX_API_KEY and sends authenticated outbound ranking API requests to redfox.hk. <br>
Mitigation: Install only if you trust RedFoxHub with the key, configure the key as an environment variable, and avoid exposing it in code, prompts, logs, or generated files. <br>
Risk: Accepting a subscription prompt may create recurring automation that continues to call the service and send ranking updates. <br>
Mitigation: Review the subscription prompt, schedule, target niche, and delivery behavior before approving recurring updates. <br>
Risk: Ranking outputs are based on periodic RedFox data and may differ from real-time Xiaohongshu platform state. <br>
Mitigation: Treat rankings as decision-support data and verify important creator, brand, or investment decisions against current source data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/xiaohongshu-top-account) <br>
- [Xiaohongshu ranking API documentation](artifact/references/api_docs.md) <br>
- [Composite scoring rules](artifact/references/score_rules.md) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox Xiaohongshu ranking API endpoint](https://redfox.hk/story/api/xhsData/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown ranking tables, HTML report files, subscription guidance, and shell/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default display is TOP 20; full TOP 50 can be requested with an HTML report. Outputs depend on RedFox API availability and REDFOX_API_KEY access.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
