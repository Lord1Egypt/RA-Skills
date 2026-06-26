## Description: <br>
公众号热门账号推荐帮助用户快速获取微信公众号综合实力TOP50榜单，支持日榜、周榜、月榜和垂直领域筛选，并提供互动指标、榜单解读、HTML可视化报告和定期推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as WeChat account operators, MCN teams, brand marketers, and content entrepreneurs use this skill to query TOP50 WeChat official account rankings, compare engagement metrics, generate analysis, export HTML reports, and subscribe to recurring ranking updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read shell profile files while looking for REDFOX_API_KEY. <br>
Mitigation: Set REDFOX_API_KEY only in the active environment for the session, and avoid storing the key in shell startup files when using this skill. <br>
Risk: The skill calls redfox.hk with a sensitive API key. <br>
Mitigation: Use a scoped or revocable RedFoxHub key when available, monitor key usage, and rotate the key if it may have been exposed. <br>
Risk: Subscription behavior is offered without clear persistence or cancellation controls in the evidence. <br>
Mitigation: Enable subscriptions only after confirming how the client stores, sends, and cancels recurring pushes. <br>
Risk: Generated HTML report files may contain ranking data intended for operational analysis. <br>
Mitigation: Review generated files before sharing or publishing them, especially when reports are used for client or competitor tracking. <br>


## Reference(s): <br>
- [Core Workflow](references/core_workflow.md) <br>
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [ClawHub Skill Page](https://clawhub.ai/if530770/wechat-power-ranking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown ranking tables and analysis, JSON from helper scripts, and optional HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for RedFoxHub API access; report generation can reuse a prefetched JSON file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
