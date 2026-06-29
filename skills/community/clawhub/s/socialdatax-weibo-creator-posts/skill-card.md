## Description: <br>
用于微博创作者数据、微博创作者内容列表、近期发布、内容调研和创作者内容分析。覆盖 Weibo creator posts，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Weibo creator post lists through SocialDataX, then summarize recent publishing activity, content style, interaction counts, media links, and author facts when present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external SocialDataX CLI with the user's SOCIALDATAX_API_KEY. <br>
Mitigation: Confirm the user trusts the SocialDataX npm package and service before installing or running it, and keep the API key in the documented SOCIALDATAX_API_KEY environment variable. <br>
Risk: Using --all or broad pagination can retrieve large creator-post collections. <br>
Mitigation: Use --max-items or bounded page counts when the user wants to limit retrieval volume. <br>


## Reference(s): <br>
- [SocialDataX API access](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-creator-posts) <br>
- [Publisher profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and summaries of JSON data returned by the SocialDataX CLI or MCP tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY plus node and npm; CLI calls return JSON with platform, tool, arguments, data, pagination, and item counts when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
