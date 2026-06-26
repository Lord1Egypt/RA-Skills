## Description: <br>
AI 新闻聚合与热度排序技能，覆盖产品发布、研究论文、行业动态、融资并购、开源项目更新和社区传播，并输出中文摘要、热度分级与来源链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npm-ued](https://clawhub.ai/user/npm-ued) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, product teams, engineers, and business readers use this skill to request Chinese AI news roundups with source links, cross-checking, deduplication, heat ranking, and impact notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent performs multiple public web searches and may surface inaccurate, stale, or low-signal news if sources are weak. <br>
Mitigation: Require source links, cross-check important items against authoritative or mainstream sources, and keep unverified community-only items in the observation list. <br>
Risk: Ambiguous AI-related questions could trigger a news roundup when the user wanted another type of help. <br>
Mitigation: Use this skill for news requests; for non-news AI tasks, invoke a more specific skill or ask the user to clarify. <br>


## Reference(s): <br>
- [推荐新闻源](references/sources.md) <br>
- [信源目录](references/source-catalog.md) <br>
- [检索词矩阵](references/search-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown news briefing with ranked items, summaries, source links, observation list, and collection statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is Chinese; default depth is standard, with quick and deep modes available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
