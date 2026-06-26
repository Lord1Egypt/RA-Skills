## Description: <br>
Stock Data Monorepo is a collection of four China A-share market data skills for volume, top gainers, stock themes, and theme-event analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-analysis agents use this skill to retrieve China A-share market metrics, top gainers, stock themes, and related news events for stock-daily-report workflows or standalone market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make external market and news queries through browser automation and data libraries. <br>
Mitigation: Run it only in environments where those outbound queries are approved, and review generated reports before acting on them. <br>
Risk: The skill can create persistent local report and data files in Desktop or workspace locations. <br>
Mitigation: Confirm output paths before execution and review generated files for sensitive or stale information. <br>
Risk: The security summary notes OpenClaw CLI or subagent workflows and under-disclosed fallback data behavior. <br>
Mitigation: Use the skill in a trusted workspace, inspect planned commands, and verify timestamps and source quality before relying on financial analysis. <br>


## Reference(s): <br>
- [Stock Data Monorepo ClawHub page](https://clawhub.ai/shinelp100/stock-data-monorepo) <br>
- [README](README.md) <br>
- [THS stock themes implementation reference](ths-stock-themes/references/implementation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON data files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Desktop or workspace report files and depends on external market and news data sources.] <br>

## Skill Version(s): <br>
1.2.5 (source: ClawHub release metadata; artifact package.json reports 1.2.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
