## Description: <br>
帮助用户追踪小红书账号日榜、周榜和月榜涨粉数据，支持查询、榜单图片生成、Excel 导出和订阅推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, MCN operators, creators, and content operations teams use this skill to inspect Xiaohongshu follower-growth rankings across fixed categories, export data, generate shareable ranking images, and configure recurring ranking notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ranking data may be fetched without normal HTTPS identity verification. <br>
Mitigation: Install only when this network behavior is acceptable, and avoid using the skill for sensitive or high-assurance data workflows. <br>
Risk: Notification and subscription features may store contact details or delivery configuration locally. <br>
Mitigation: Review local subscription and delivery configuration storage before entering sensitive contact details or production messaging credentials. <br>
Risk: Generated Excel and image files may be copied to the Desktop. <br>
Mitigation: Run exports in an environment where Desktop file placement is acceptable, and review generated files before sharing them externally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/rednote-ranking-data) <br>
- [Publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [Subscription tiers reference](references/subscription_tiers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON ranking data, Excel exports, and PNG ranking images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports category, ranking period, date, limit, output path, and subscription delivery settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
