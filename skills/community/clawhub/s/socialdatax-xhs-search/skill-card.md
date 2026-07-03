## Description: <br>
用于小红书数据分析、小红书笔记搜索、关键词检索、内容调研、竞品分析和趋势研究。覆盖 Xiaohongshu / XHS / RedNote note search，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, marketers, researchers, and content teams use this skill to search Xiaohongshu / XHS / RedNote notes for keyword research, topic discovery, content planning, competitor research, market observation, and trend scanning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and the SOCIALDATAX_API_KEY are sent to SocialDataX tooling. <br>
Mitigation: Install and run the skill only when SocialDataX is a trusted service for the intended use case, and provide the API key through the documented SOCIALDATAX_API_KEY environment variable. <br>
Risk: Returned note URLs may contain xsec_token query parameters that could be sensitive if broadly shared or logged. <br>
Mitigation: Avoid unnecessary redistribution or logging of full returned note URLs, and share results only with audiences authorized to receive those links. <br>
Risk: Recent-topic findings may not represent complete platform coverage beyond fetched pages. <br>
Mitigation: Use bounded page and recency parameters such as --pages and --since-days, and describe findings as observations from the fetched result set. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-search) <br>
- [SocialDataX homepage](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/devinchen2014) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and summarized XHS search evidence] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserve returned note URLs and pagination tokens exactly; recent topic research is bounded by fetched pages.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
