## Description: <br>
中国 A 股/港股只读数据查询与分析技能，支持将自然语言需求映射到 stocks 接口，并输出行情、基本面、指数和文本数据的结构化分析结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roamer-remote](https://clawhub.ai/user/roamer-remote) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to query public historical A-share and Hong Kong stock data, then review structured market, fundamental, index, text-source, and risk analysis. It is intended for research support and does not place trades or provide guaranteed investment outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial analysis may rely on historical market data plus external web or forum sources, which can be incomplete, delayed, or misleading. <br>
Mitigation: Treat outputs as research support, verify important claims against source data, and keep the skill's non-investment-advice framing in user-facing analysis. <br>
Risk: The skill requires TAX_API_KEY, a sensitive credential. <br>
Mitigation: Configure TAX_API_KEY only through the agent platform's secret or environment-variable mechanism and do not paste, echo, store, or request the key in chat. <br>
Risk: Notification pushing and cross-agent processing are described without detailed user-control boundaries. <br>
Mitigation: Require explicit user confirmation before sending notifications or sharing results beyond the current analysis workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roamer-remote/stocks-query-base-skill) <br>
- [TAX API homepage](https://tax.yyyou.top/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API query guidance, Configuration guidance] <br>
**Output Format:** [Markdown structured analysis with API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAX_API_KEY configured as a secret; outputs should include risk notes and a non-investment-advice disclaimer for investment-related analysis.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
