## Description:

Recomputes true gross profit and margin per SKU from price, cost, freight, platform commission, ad spend, return loss, and FX conversion, then flags mismatches, low-margin rows, totals issues, duplicate rows, blanks, and negative values with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, cross-border operators, and finance reviewers use this skill during monthly close to recalculate SKU-level gross profit and margin from exported table data. It helps identify rows where platform or spreadsheet profit figures omit freight, advertising, returns, or FX effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads the local file path supplied with --input, so selecting the wrong file can expose or analyze unintended SKU data.

Mitigation: Review the input file path and contents before execution, and run it only on files intended for SKU profit checking.

Risk: The calculations cover only the fields provided in the SKU profit table and do not replace full accounting, tax, inventory, or market analysis.

Mitigation: Use the output as a reconciliation aid and review omitted costs, accounting treatment, taxes, and business decisions separately.

Risk: The packaged output is Chinese-language unless the publisher adds localization.

Mitigation: Confirm that reviewers can read the Chinese output or translate the results before relying on them operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/sku-profit-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Chinese-language plain text or JSON with SKU profit findings, calculated values, omitted checks, and source line references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs against a user-supplied SKU profit table and reports insufficient input instead of fabricating conclusions.]

## Skill Version(s):

1.0.41 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
