## Description: <br>
Generates Korean quotes and tax invoices, manages client and item records, calculates VAT and totals, and exports invoice documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, freelancers, and business operators use this skill to create quotes and tax invoices, maintain reusable client and item data, and generate local invoice files for customer billing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and emits sensitive business, client, invoice, tax, and banking data in local data and output files. <br>
Mitigation: Install only in a trusted local workspace and treat the data and output folders as sensitive. <br>
Risk: Untrusted client names, item descriptions, or notes can flow into generated HTML or Markdown documents. <br>
Mitigation: Use trusted input data until generated HTML and Markdown escaping and output path constraints are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/unified-invoice) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with CLI commands; generated invoice artifacts are HTML, PDF, and Markdown where supported.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include client, business, invoice amount, tax, and bank-account data.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata; artifact frontmatter and package.json show 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
