## Description:

Multi-platform Order Profit Calculator - upload order exports from any e-commerce platform or ERP, get instant profit reports by order, store, SKU, and platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersplind92](https://clawhub.ai/user/jeffersplind92)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, analysts, and agents use this skill to inspect order-export spreadsheets, map relevant columns, and produce profit summaries by order, platform, store, and SKU.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order-export spreadsheets may contain customer, sales, or other sensitive business data.

Mitigation: Use local processing when possible, provide only intended workbooks, and avoid the hosted API option until the publisher documents what data is sent and retained.

Risk: Markdown reports can include text derived from workbook cells, which may affect report rendering when workbooks are untrusted.

Mitigation: Review generated Markdown before sharing or rendering it in privileged contexts, especially when the workbook came from an external source.

Risk: Profit calculations depend on available columns and correct field mapping.

Mitigation: Inspect header analysis and field-map JSON, and compare calculated profit with platform-declared values when those fields are present.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/jeffersplind92/skills/seller-profit-calculator-max)
- [Publisher Profile](https://clawhub.ai/user/jeffersplind92)
- [YK-Global Website](https://yk-global.com)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report printed to stdout, optional JSON result file, and field-map JSON guidance for parser commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Excel .xlsx and .xls order exports; CSV and settlement reports are not supported in version 1.0.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
