## Description: <br>
股票深度分析（18维度融合版）：基本面估值+实战交易双重视角，支持A股/港股/美股，输出完整9部分飞书文档报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dennisxiaoding](https://clawhub.ai/user/dennisxiaoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market researchers use this skill to analyze A-share, Hong Kong, and U.S. stocks through an 18-dimension framework and produce a structured Feishu report with ratings, position guidance, target price ranges, stop-loss levels, data sources, and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock analysis may be incorrect, incomplete, outdated, or unsuitable as financial advice. <br>
Mitigation: Review the generated report before relying on it financially, verify cited data against authoritative market sources, and retain the skill's investment-risk disclaimers. <br>
Risk: The skill writes report content to a Feishu workspace and could create or share an incomplete report. <br>
Mitigation: Confirm the Feishu document content after creation and before sharing, including the artifact's required checks for non-empty content and sufficient block count. <br>


## Reference(s): <br>
- [18维度分析框架详细说明](references/analysis-framework.md) <br>
- [数据源说明](references/data-sources.md) <br>
- [9部分报告结构详细规范](references/report-structure.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dennisxiaoding/tbog-stock-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/dennisxiaoding) <br>
- [东方财富网](https://www.eastmoney.com/) <br>
- [同花顺](https://www.10jqka.com.cn/) <br>
- [巨潮资讯](http://www.cninfo.com.cn/) <br>
- [Yahoo Finance](https://finance.yahoo.com/) <br>
- [SEC EDGAR](https://www.sec.gov/edgar.shtml) <br>
- [港交所披露易](https://www.hkexnews.hk/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report content plus a concise text conclusion and Feishu document link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should separate facts, forecasts, and subjective judgment; cite data sources; and include financial risk disclaimers.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
