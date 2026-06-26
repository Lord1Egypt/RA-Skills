## Description: <br>
Multi-platform order profit calculator that lets users upload e-commerce or ERP order exports and generate profit reports by order, store, SKU, and platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersplind92](https://clawhub.ai/user/jeffersplind92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to analyze e-commerce order exports, map spreadsheet columns, and calculate order-level and aggregate profit. It is intended for merchant operations workflows that need local Markdown or JSON profit reporting from Excel exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order exports may contain customer, order, and store financial data. <br>
Mitigation: Start in local mode with redacted or synthetic spreadsheets, and only process sensitive merchant data after confirming handling requirements. <br>
Risk: The README documents a hosted API key path, but the artifact does not provide clear hosted-processing behavior. <br>
Mitigation: Do not set PROFIT_API_KEY or use the documented API path unless the publisher supplies updated implementation and data-transfer documentation. <br>
Risk: Profit results depend on spreadsheet headers, field mapping, and the columns present in each export. <br>
Mitigation: Review the header analysis and field_map before using reports for operational or pricing decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jeffersplind92/seller-profit-calculator-max) <br>
- [YK-Global Official Site](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report printed to stdout, with optional JSON and Markdown output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Excel workbooks and can use an agent-provided field_map JSON for column mapping.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
