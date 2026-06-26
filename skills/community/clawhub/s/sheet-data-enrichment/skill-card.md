## Description: <br>
Enrich spreadsheet rows by fetching linked URLs or APIs to fill missing values, then aggregate the completed data into summary sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylinr](https://clawhub.ai/user/kylinr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to enrich spreadsheet rows from external sources, verify extracted values, write them back safely, and create grouped summary sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet-linked URLs or row context may be sent to external sites or APIs during enrichment. <br>
Mitigation: Confirm domains and target rows before fetching, and avoid sensitive spreadsheets unless the user has approved the external lookups. <br>
Risk: Incorrect row alignment during write-back can place extracted values in the wrong cells. <br>
Mitigation: Read the target row before writing, use explicit single-cell ranges, and review proposed write-backs before applying them. <br>
Risk: Ambiguous or incomplete web extraction can produce incorrect enriched data. <br>
Mitigation: Flag ambiguous results for manual review, verify samples before batch application, and avoid guessing when source data is unclear. <br>


## Reference(s): <br>
- [Extraction Patterns](references/extraction-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kylinr/sheet-data-enrichment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with spreadsheet write plans, extracted values, verification notes, and summary sheet specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include row-by-row enrichment results, manual-review flags, grouping dimensions, subtotals, and grand totals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
