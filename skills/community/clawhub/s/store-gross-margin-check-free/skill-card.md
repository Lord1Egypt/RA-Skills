## Description:

门店销售与成本毛利表逐项核对（销售额与收款勾稽、成本差异复算、毛利率逐行复算、损耗率超限、重复与空缺），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Store finance staff, accountants, and store managers use this skill during monthly close, operating analysis, and inventory variance review to check store sales-and-cost gross margin tables. It identifies table-level reconciliation issues, missing required fields, duplicate rows, margin-rate inconsistencies, cost variances, and loss-rate threshold findings with source row numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input tables may contain sensitive store financial or operating data.

Mitigation: Run the reviewed local CLI flow and avoid adding network transfer, logging, or persistence around the supplied input files.

Risk: The skill checks table arithmetic and reconciliation only, not accounting policy, tax treatment, pricing strategy, inventory controls, or root causes of loss.

Mitigation: Treat findings as review signals and have qualified finance or operations staff confirm business decisions and policy judgments.

Risk: The free version omits gross-margin change attribution and ranked remediation outputs.

Mitigation: Use the reported scope fields to confirm which checks ran and do not treat a clean result as a complete gross-margin audit.

Risk: Incomplete or unrecognized input headers cause insufficient-input results rather than conclusions.

Mitigation: Provide the required table headers and source rows before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/store-gross-margin-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON from a local Node.js CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source row numbers; insufficient input returns missing fields instead of conclusions.]

## Skill Version(s):

1.0.8 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
