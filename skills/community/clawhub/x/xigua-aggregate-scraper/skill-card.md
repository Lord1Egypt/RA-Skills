## Description: <br>
西瓜视频数据查询助手。覆盖视频详情、用户数据、搜索、评论等全功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content teams, researchers, and developers use this skill to query Xigua video details, user profiles, post lists, search results, play URLs, and comments through MaxHub APIs for content research and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MaxHub API key and sends video IDs, user IDs, search terms, and comment queries to www.aconfig.cn. <br>
Mitigation: Install only when that data sharing is acceptable, store MAXHUB_API_KEY in the configured secret or environment mechanism, and avoid pasting key values into prompts or shared files. <br>
Risk: Security evidence notes that the instructions also reference Douyin and Xiaohongshu API paths despite the skill being presented as Xigua-focused. <br>
Mitigation: Review the skill before installation and remove or correct non-Xigua path references if a strictly Xigua-only workflow is required. <br>
Risk: API calls depend on third-party MaxHub service availability, permissions, and endpoint behavior. <br>
Mitigation: Treat returned data as reference material, handle 401/403/404/429/5xx responses explicitly, and disclose unavailable or empty results to users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/xigua-aggregate-scraper) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Video & User API reference](references/api-video-user.md) <br>
- [Parameter mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables, summaries, and optional curl command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese or English output; keeps API key values out of responses.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
