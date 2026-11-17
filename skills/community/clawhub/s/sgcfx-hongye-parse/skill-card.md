## Description:

Parses Hongye SGCFX construction cost files and exports bills of quantities, labor/material/machinery summaries, fee breakdowns, and submitted-versus-reviewed comparisons to Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kormendierijon681-oss](https://clawhub.ai/user/kormendierijon681-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and construction cost engineers use it to extract bill-of-quantities data, material summaries, and fee breakdowns from Hongye SGCFX project files, and to compare submitted and reviewed versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Previous working files or exports may be overwritten.

Mitigation: Use a fresh working directory and separate output folder for each project, retain the original archives, and verify version labels and totals before relying on exports.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kormendierijon681-oss/skills/sgcfx-hongye-parse)

## Skill Output:

**Output Type(s):** [Excel workbooks, CSV files, Validation summaries]

**Output Format:** [Excel (.xlsx) workbooks and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes quantity, price, and total reconciliation checks where supported.]

## Skill Version(s):

2.0.2 (source: server-resolved release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
