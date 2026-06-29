## Description: <br>
用于微博数据分析、微博热搜、微博内容研究、关键词观察、内容调研、竞品分析和趋势研究，覆盖 Weibo hot-search and post research，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, analysts, and developers use this skill to fetch Weibo hot-search lists and keyword post results through SocialDataX for content research, competitor analysis, and trend scanning. The skill helps agents summarize observed rankings, authors, URLs, engagement counts, and publish times while keeping evidence separate from interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may run a third-party npm package and send user queries plus SOCIALDATAX_API_KEY to SocialDataX for Weibo data access. <br>
Mitigation: Use a dedicated API key when possible, configure only SOCIALDATAX_API_KEY for this skill, and review the npm package and publisher when stronger supply-chain assurance is required. <br>
Risk: Weibo hot-search and keyword results are live social-media observations that may be incomplete, paginated, or change quickly. <br>
Mitigation: Summarize visible evidence separately from interpretation and include IDs, URLs, counts, publish times, and pagination context when traceability matters. <br>


## Reference(s): <br>
- [SocialDataX API access](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Weibo post IDs, URLs, author facts, interaction counts, publish times, and pagination tokens when traceability is needed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
