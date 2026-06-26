## Description: <br>
Turn messy service pricing notes into professional quotes, SOW line items, and invoice drafts with assumptions clearly surfaced. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external service providers, and operators use this skill to turn raw scope, rate, timeline, tax, discount, and payment-term inputs into draft quote tables, SOW line items, invoice drafts, assumptions, and exclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft quotes or invoices can contain incorrect amounts, taxes, discounts, terms, assumptions, or exclusions if the inputs are incomplete or ambiguous. <br>
Mitigation: Review all amounts, taxes, discounts, terms, assumptions, and exclusions before sending outputs externally. <br>
Risk: The helper script writes a JSON output file to a path chosen at runtime. <br>
Mitigation: Run the helper only with input and output paths the user intentionally selects. <br>
Risk: Draft business documents may be mistaken for final legal, financial, or contractual decisions. <br>
Mitigation: Keep outputs labeled as drafts and mark uncertain fields as pending confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/quote-invoice-workbench) <br>
- [README](artifact/README.md) <br>
- [Example prompt](artifact/examples/example-prompt.md) <br>
- [Smoke test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts and optional JSON files from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft outputs should surface assumptions, exclusions, taxes, discounts, deposits, milestones, and unresolved fields for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
