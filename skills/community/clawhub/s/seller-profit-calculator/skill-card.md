## Description: <br>
Multi-platform Order Profit Calculator that processes e-commerce or ERP order exports and returns profit reports by order, store, SKU, and platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to analyze Excel order exports from e-commerce platforms or ERPs, map platform-specific fields, and calculate revenue, costs, net profit, and margin by order, store, SKU, and platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order exports and generated reports can contain sensitive order, store, SKU, financial, or customer-related data. <br>
Mitigation: Use only authorized exports, prefer redacted or minimal spreadsheets, and treat stdout, JSON, Markdown, and header-analysis outputs as sensitive. <br>
Risk: The README describes a hosted API path that is not documented with data handling, storage, or retention details in the provided evidence. <br>
Mitigation: Use the local workflow by default and avoid the hosted API path unless a future release documents what data is sent, stored, and retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiji0802/seller-profit-calculator) <br>
- [Publisher Profile](https://clawhub.ai/user/qiji0802) <br>
- [YK Global Website](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports printed to stdout, optional JSON result files, optional Markdown files, and JSON header-analysis files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local Excel .xlsx and .xls order exports; optional field-map JSON can be supplied inline or from a file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
