## Description: <br>
Queries A-share and Hong Kong stock valuation data, including PE, PB, PS, discounted cash flow style measures, fair price, margin of safety, and valuation labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfei619](https://clawhub.ai/user/chenfei619) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agent workflows use this skill to retrieve structured valuation reports for supported A-share and Hong Kong stock codes. The reports are for informational research and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries send stock codes, and any configured STOCK_VALUATION_AUTH token, to tz.smxqx.tech. <br>
Mitigation: Install only when that data sharing is acceptable, and use a dedicated token with limited exposure where possible. <br>
Risk: Valuation reports may be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational research and require human financial judgment before making investment decisions. <br>
Risk: The artifact includes a public fallback API token that may be rate-limited or unsuitable for private deployments. <br>
Mitigation: Configure STOCK_VALUATION_AUTH explicitly and monitor failures or rate-limit responses. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chenfei619/sz-stock-valuation) <br>
- [API field reference](references/api_fields.md) <br>
- [Stock code format reference](references/stock_code_format.md) <br>
- [Stock valuation API endpoint](https://tz.smxqx.tech/api/stock/valuation/detail) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, API Calls] <br>
**Output Format:** [Markdown valuation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current quote metrics, valuation ratios, fair value estimates, margin of safety, valuation labels, and an investment-advice disclaimer when data is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
