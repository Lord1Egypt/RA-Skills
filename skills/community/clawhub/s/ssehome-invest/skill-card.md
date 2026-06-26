## Description: <br>
基于 baostock 金融数据库和 tavily-search 智能搜索的股票投资分析技能，提供完整的多时间框架技术分析、市场热点资讯追踪和投资报告生成功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssehome](https://clawhub.ai/user/ssehome) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts can use this skill to generate A-share stock research reports that combine baostock market data, technical indicators, Tavily news search, sentiment notes, and Markdown report output. The generated analysis is for research support and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package ships an apparent hard-coded Tavily API key and conflicting credential guidance. <br>
Mitigation: Review or remove tavily_config.py before installing, do not rely on the bundled key, and configure a user-controlled Tavily key only when the search-query exposure is acceptable. <br>
Risk: The skill sends stock and news search queries to external services when optional Tavily search is enabled. <br>
Mitigation: Disable Tavily search or use an approved API key and environment policy when query confidentiality matters. <br>
Risk: Runtime dependencies are broad minimum-version ranges. <br>
Mitigation: Install in an isolated environment and pin dependencies before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssehome/ssehome-invest) <br>
- [baostock documentation](https://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5) <br>
- [Tavily documentation](https://docs.tavily.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated stock reports under a data directory when executed.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release and SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
