## Description: <br>
A股板块实时研报。全球新闻→A股映射、板块趋势研判、美股关联、利好利空、大事件提醒。零配置可用，输出兼容飞书/扣子/Markdown平台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarveyZzzz](https://clawhub.ai/user/HarveyZzzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to generate concise A-share sector research reports, AI market briefings, and anomaly monitoring summaries from public market and news data. It is intended for informational market commentary and not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public market and news services. <br>
Mitigation: Install and run it only in environments where those network requests are acceptable. <br>
Risk: TAVILY_API_KEY can be supplied for enhanced news search. <br>
Mitigation: Use a key intended for this tool and manage it as a normal secret. <br>
Risk: Generated stock and sector commentary may be incomplete or unsuitable for financial decisions. <br>
Mitigation: Treat outputs as informational commentary, verify important claims, and do not treat reports as investment advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HarveyZzzz/stockselectionmodel) <br>
- [AI 股票内参 — 研判 Prompt](artifact/references/analysis_prompt.md) <br>
- [板块趋势研判 Prompt](artifact/references/sector_prompt.md) <br>
- [数据源优先级](artifact/references/source_list.md) <br>
- [AI 概念 A 股映射表](artifact/references/stock_mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown research reports with tables, short text summaries, and optional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include sector trend, news, gainers and losers, US-stock links, positive and negative factors, events, watch points, and risk notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
