## Description: <br>
用于微博评论分析、微博评论回复、微博评论洞察、用户反馈、口碑分析、痛点总结和内容讨论分析。覆盖 Weibo comments and comment replies，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to retrieve Weibo first-level comments and replies through SocialDataX, then summarize sentiment themes, pain points, objections, FAQs, and discussion patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the socialdatax-skills npm package with SOCIALDATAX_API_KEY, which may expose sensitive API access if run in an untrusted or sensitive environment. <br>
Mitigation: Install only when SocialDataX Weibo comment analysis is intended, protect the API key, and review the npm package or source before use in sensitive environments. <br>
Risk: The skill retrieves external Weibo comment data for analysis, so conclusions may be incomplete when only one page is fetched or when comments are empty. <br>
Mitigation: State whether results cover one page or multiple pages, preserve pagination tokens unchanged, and treat empty comments as a possible successful result. <br>


## Reference(s): <br>
- [SocialDataX](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-comments) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON data from CLI or MCP calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY, node, and npm; comment pagination uses opaque page tokens that should be passed back unchanged.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
