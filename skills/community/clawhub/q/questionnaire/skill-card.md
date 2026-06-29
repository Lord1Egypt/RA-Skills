## Description: <br>
A Chinese-language BI requirements cleanup skill that processes uploaded question and reference documents to extract metrics, dimensions, and filter conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hht1ng](https://clawhub.ai/user/hht1ng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, BI developers, and product teams use this skill to prepare BI dashboard requirements by filling metric, dimension, and filter-condition fields in uploaded question workbooks. It can also create a metric-dimension matrix while using optional business knowledge, metric-dimension, data dictionary, and table-structure documents as references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read uploaded business glossary, data dictionary, table-structure, and requirement documents in full. <br>
Mitigation: Use it only with documents that are approved for the execution environment and remove unnecessary sensitive content before upload. <br>
Risk: Automated metric, dimension, and filter-condition extraction may be incomplete or incorrect for ambiguous requirement questions. <br>
Mitigation: Review the filled workbook columns, unresolved prompts, and generated metric-dimension matrix before using the results for BI design or implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hht1ng/skills/questionnaire) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured text for workbook fields and a metric-dimension matrix] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write results back into the provided spreadsheet while preserving the original workbook style.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
