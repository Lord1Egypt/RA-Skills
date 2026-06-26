## Description: <br>
Provides a stock-investment advisor workflow for real-time market data collection, multi-source research, chart interpretation, collaborative analysis, and professional report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gouyujun](https://clawhub.ai/user/gouyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment research agents use this skill to analyze A-share, Beijing Stock Exchange, Hong Kong, and U.S. equities, compare stocks or sectors, interpret chart screenshots, and produce concise summaries or Feishu investment reports. Outputs are for reference and should include risk disclosures and disclaimers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use web searches and financial-data services, so outputs can depend on external data quality, freshness, and availability. <br>
Mitigation: Confirm important market data against authoritative sources and preserve the skill's requirement to state when data is unavailable rather than fabricating values. <br>
Risk: Feishu cloud reports may contain stock-analysis context, portfolio details, or chart screenshots. <br>
Mitigation: Avoid submitting sensitive portfolio information or private screenshots unless external cloud reporting is acceptable for the user or organization. <br>
Risk: Optional helper scripts and data-source integrations may require credentials such as API tokens. <br>
Mitigation: Keep tokens out of shared files and logs, and review optional helper scripts before installing or extending them. <br>
Risk: Generated investment analysis could be mistaken for personalized financial advice. <br>
Mitigation: Keep the report disclaimer and risk-warning sections, and treat outputs as reference material for independent decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gouyujun/stock-investment-advisor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, Feishu document reports, JSON from helper scripts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web searches, financial-data services, chart screenshots, and Feishu cloud document creation; includes risk disclosures and disclaimers when producing reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact notes v1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
