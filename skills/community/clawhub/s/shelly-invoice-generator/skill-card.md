## Description: <br>
Generate professional invoices in Markdown or HTML by specifying client details, line items, tax, currency, dates, invoice numbers, and output format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers, small businesses, and operations teams can use this skill to create itemized invoices from command-line inputs, then emit a clean Markdown invoice or a print-ready HTML invoice. It is useful when an agent needs repeatable invoice generation with configurable tax, currency, due dates, sender details, client details, and invoice numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local shell script to generate invoices. <br>
Mitigation: Install and run it only in environments where local shell execution is acceptable, and review the script before operational use. <br>
Risk: Generated HTML includes caller-provided client and item text. <br>
Mitigation: Use trusted invoice inputs or sanitize text before rendering, opening, or sharing HTML output. <br>
Risk: The output path can write invoice content to a local file. <br>
Mitigation: Use explicit safe output paths and avoid paths that could overwrite important files. <br>
Risk: Invoice calculations depend on the bc command-line utility. <br>
Mitigation: Confirm bc is installed before relying on generated totals. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/claudiodrusus/shelly-invoice-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/claudiodrusus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML, shell commands, files] <br>
**Output Format:** [Markdown invoice or print-ready HTML invoice, written to stdout or a user-specified output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local shell environment and bc for arithmetic; HTML output should be treated as generated content from supplied invoice text.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
