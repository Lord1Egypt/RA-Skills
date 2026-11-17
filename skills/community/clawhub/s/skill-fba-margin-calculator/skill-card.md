## Description:

Calculates Amazon UAE FBA fees, net margin, and dangerous-goods risk for CJ Dropshipping product candidates, ranks SKUs by margin percentage, and generates markdown and JSON reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to compare CJ Dropshipping product candidates before Amazon UAE FBA launch decisions. It helps estimate landed cost, Amazon fees, referral fees, net margin, and DG-related fulfillment risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Estimated FBA fees, referral percentages, exchange rates, and DG status may differ from current Amazon UAE Seller Central values.

Mitigation: Verify FBA fees, DG classification, referral category, and current pricing in Seller Central before ordering samples or sending inventory to FBA.

Risk: The skill can write local markdown and JSON reports to the output path supplied by the user.

Mitigation: Review the product data and output base path before execution, and run the calculator in the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-fba-margin-calculator)
- [Publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report and JSON results, with optional shell commands for local execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks products by margin percentage and can write paired .md and .json report files when an output base path is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
