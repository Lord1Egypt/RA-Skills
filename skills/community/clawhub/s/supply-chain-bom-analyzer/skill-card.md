## Description: <br>
供应链 BOM 数据分析 extracts, cleans, and aligns hardware BOM data from supplier quotes and Excel/CSV files, then produces time-based material demand forecast summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[git-Surellc](https://clawhub.ai/user/git-Surellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Supply-chain, procurement, and engineering users use this skill to analyze supplier quotes and BOM spreadsheets, extract physical hardware materials, normalize equivalent items, and aggregate quantities by project delivery timeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supplier quotes and BOM spreadsheets may contain sensitive business data. <br>
Mitigation: Only provide files the user is authorized to process, and run the skill in an approved agent environment. <br>
Risk: Incorrect item normalization, quantity extraction, or timeline mapping could distort demand forecasts. <br>
Mitigation: Review generated tables against the source documents and confirm unresolved items, missing quantities, and project delivery dates before relying on the output. <br>


## Reference(s): <br>
- [Data Extraction Rules](references/extraction-rules.md) <br>
- [Material Standardization Mapping](references/material-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown tables and concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on physical material rows, standardized product names, summed quantities, and timeline-based demand columns.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
