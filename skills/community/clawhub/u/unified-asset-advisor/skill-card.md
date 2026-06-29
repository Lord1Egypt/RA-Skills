## Description: <br>
Unified Asset Advisor helps agents generate China-focused asset-allocation analysis from macroeconomic data, sector trends, asset-cycle logic, instrument recommendations, and futures/options strategy guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianchunhui](https://clawhub.ai/user/bianchunhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to ask an agent for China-focused macro, industry, and asset-allocation reports across equities, bonds, commodities, funds, futures, and options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate actionable investment ideas, including futures and options strategies, without assessing suitability, risk tolerance, or regulatory compliance. <br>
Mitigation: Treat outputs as research until reviewed by a qualified human, and confirm suitability, risk limits, and applicable rules before acting. <br>
Risk: Public market data can be incomplete, delayed, unavailable, or inconsistent across AKShare, TDX, and web-search sources. <br>
Mitigation: Cross-check key macro and market values against authoritative sources, keep source timestamps, and label fallback or static data in reports. <br>
Risk: Generated HTML, Markdown, and Excel reports may appear definitive even when based on transient market conditions. <br>
Mitigation: Review reports before distribution and preserve confidence levels, stop-loss references, and risk notes in the final output. <br>


## Reference(s): <br>
- [Unified Asset Advisor on ClawHub](https://clawhub.ai/bianchunhui/unified-asset-advisor) <br>
- [Asset Cycle Logic](references/asset_cycle_logic.md) <br>
- [Futures Options Guide](references/futures_options_guide.md) <br>
- [SW Industry List](references/sw_industry_list.md) <br>
- [Report Template](assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown reports, HTML reports, Excel workbooks, JSON data, and inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce three report artifacts: HTML, Markdown, and an 8-sheet Excel workbook.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
