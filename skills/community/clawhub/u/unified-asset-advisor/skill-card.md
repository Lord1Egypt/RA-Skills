## Description:

Unified Asset Advisor guides an agent through China-market macro analysis, asset-cycle assessment, industry screening, instrument recommendations, and futures/options strategy to produce asset allocation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianchunhui](https://clawhub.ai/user/bianchunhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare China-market asset allocation research reports across macro conditions, asset classes, Shenwan industries, ETFs, funds, bonds, commodities, futures, and options. The skill is intended for investment research support, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install Python packages without pinned versions.

Mitigation: Run it in an isolated virtual environment or workspace and review or pin dependencies before installation.

Risk: The skill fetches live financial market data and produces investment, futures, and options recommendations.

Mitigation: Treat outputs as research support only, verify key data against authoritative sources, and avoid using the output as personalized financial advice.

Risk: The skill generates Excel report files from unsanitized data.

Mitigation: Review generated workbooks before sharing or opening them in sensitive environments.

## Reference(s):

- [Asset Cycle Logic](references/asset_cycle_logic.md)
- [Shenwan Industry List](references/sw_industry_list.md)
- [Futures Options Guide](references/futures_options_guide.md)
- [Markdown Report Template](assets/report_template.md)
- [HTML Report Template](assets/report_template.html)
- [ClawHub Skill Page](https://clawhub.ai/bianchunhui/skills/unified-asset-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated HTML, Markdown, and Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce an 8-sheet Excel workbook and dated asset allocation report files when dependencies and data sources are available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
