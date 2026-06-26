## Description: <br>
小红书账号榜单追踪分析工具，支持查询日榜、周榜、月榜 TOP50 排名和热门账号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brands, MCN teams, and analysts use this skill to query Xiaohongshu account rankings, filter by niche, generate ranking reports, and optionally schedule ranking updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires REDFOX_API_KEY and sends authenticated requests to RedFox's Xiaohongshu ranking API. <br>
Mitigation: Install only if you trust RedFox with the key, keep the key in the environment, and avoid exposing it in prompts, logs, or output files. <br>
Risk: The skill can create recurring ranking reminders when the user asks for subscriptions. <br>
Mitigation: Review each subscription before confirming it and cancel recurring reminders when automated ranking pushes are no longer wanted. <br>
Risk: Generated HTML reports are local files and may load a CDN script when opened for image export. <br>
Mitigation: Open generated reports only in an environment where loading that external script is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/xiaohongshu-rank-tracker) <br>
- [RedFox publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [API documentation](artifact/references/api_docs.md) <br>
- [Score rules](artifact/references/score_rules.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown ranking tables, local HTML reports, and concise setup or subscription guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for ranking API calls; HTML reports are local workspace files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
