## Description: <br>
Global landed cost calculator for traders shipping to the US. Combines live USITC tariffs, Section 232/301/AD-CVD duties, real-time exchange rates (ECB), ocean freight costs, UFLPA compliance, and customs entry fees into a single per-unit cost. Supports 18+ origin countries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoningliu1-lang](https://clawhub.ai/user/zhaoningliu1-lang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External traders, importers, ecommerce operators, and trade-compliance teams use this skill to estimate US landed costs from HTS classification, country of origin, tariffs, exchange rates, freight, customs fees, and compliance flags. It is intended for planning and analysis, with final import obligations verified by a licensed customs broker or qualified counsel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a separate local backend and dependencies before it can answer tariff and landed-cost questions. <br>
Mitigation: Review the backend repository and dependencies before installing, and run the backend in an isolated virtual environment. <br>
Risk: Tariff, AD/CVD, compliance, exchange-rate, and freight outputs can be estimates or change-sensitive. <br>
Mitigation: Verify import obligations with a licensed customs broker or qualified counsel before making business decisions. <br>
Risk: Optional paid provider API keys may expose account access if configured carelessly. <br>
Mitigation: Only set provider API keys when needed, keep them out of shared prompts or files, and scope them according to provider guidance. <br>


## Reference(s): <br>
- [Trade Compass source repository](https://github.com/zhaoningliu1-lang/tariff-watch) <br>
- [USITC HTS Schedule](https://hts.usitc.gov/) <br>
- [ECB exchange rates via Frankfurter](https://www.frankfurter.app/) <br>
- [Commerce Department AD/CVD information](https://enforcement.trade.gov/antidumping/antidumping.html) <br>
- [CBP UFLPA Entity List](https://www.cbp.gov/trade/forced-labor/UFLPA) <br>
- [Freightos API](https://www.freightos.com/api/) <br>
- [ExchangeRate-API](https://www.exchangerate-api.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown] <br>
**Output Format:** [Markdown with API endpoint examples, shell commands, and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reviewed local FastAPI backend on localhost:8000; may use optional paid API keys for fuller exchange-rate and freight coverage.] <br>

## Skill Version(s): <br>
3.2.0 (source: release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
