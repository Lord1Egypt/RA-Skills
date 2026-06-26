## Description: <br>
Pricing Engine calculates B2B quotes from LME copper prices, quantity tiers, customer grades, and exchange rates, then integrates with quotation-workflow to generate quotation files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations teams use this skill to generate single-SKU or batch quotes, preview pricing, and create PDF/HTML/Excel quotation outputs. Developers can use its Node.js APIs and configuration files to connect product costs, customer discounts, exchange rates, copper costs, and quotation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute local quotation-workflow scripts through a configured workflow path. <br>
Mitigation: Install only from a trusted publisher, verify QUOTATION_WORKFLOW_ROOT points to a reviewed local directory, and use preview or DRY_RUN before production execution. <br>
Risk: Customer-linked pricing records may be written to local output or history files. <br>
Mitigation: Store output and history files in protected locations and define retention and deletion procedures before production use. <br>
Risk: Quotes can depend on cached, fallback, or simulated copper price and exchange-rate data. <br>
Mitigation: Confirm market inputs before sending binding quotations, especially after API outages or DRY_RUN testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-pricing-engine) <br>
- [Exchange rate API used by the artifact](https://open.er-api.com/v6/latest/USD) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash and JavaScript examples; runtime outputs include JSON pricing data and PDF/HTML/Excel quotation files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local configuration files, optional DRY_RUN mode, and JSONL quote history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
