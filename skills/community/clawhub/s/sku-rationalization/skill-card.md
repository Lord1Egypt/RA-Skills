## Description: <br>
Identify underperforming SKUs, recommend discontinuations, and optimize product catalog for maximum profitability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchandising, ecommerce, operations, and finance teams use this skill to analyze product catalog exports, score SKU performance, and produce keep, fix, or kill recommendations with financial impact estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags bundled helper behavior that can bypass normal sandbox protections during nested review workflows. <br>
Mitigation: Review the skill before installation and avoid enabling sandbox-bypass review behavior unless the exact target, reason, environment, and rollback path are confirmed. <br>
Risk: The skill may produce SKU discontinuation or liquidation recommendations from incomplete, seasonal, or strategically constrained catalog data. <br>
Mitigation: Validate data completeness, seasonality, new-launch status, supplier constraints, and strategic assortment overrides before acting on keep, fix, or kill recommendations. <br>


## Reference(s): <br>
- [Output Template](references/output-template.md) <br>
- [Scoring Methodology Guide](references/scoring-methodology.md) <br>
- [Liquidation Strategies Playbook](references/liquidation-strategies.md) <br>
- [SKU Rationalization Quality Checklist](assets/quality-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/leooooooow/sku-rationalization) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with scored tables, recommendations, action plans, and financial impact summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses catalog metrics such as revenue contribution, gross margin, inventory turnover, demand velocity, return rate, and days of supply.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
