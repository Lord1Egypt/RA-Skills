## Description: <br>
Generates a consolidated weekly retail trade report from 12 sales Excel files and a store mapping CSV, including regional ADA metrics, week-over-week comparisons, formatted tables, and charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuminmin](https://clawhub.ai/user/wuminmin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Retail operations and reporting teams use this skill to convert weekly channel sales spreadsheets into a single Excel workbook for regional performance review. It is intended for users who can supply the required sales files, validate store-to-region mappings, and review the generated business metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided retail sales spreadsheets and a store mapping CSV, which may contain sensitive business information. <br>
Mitigation: Run it only with files you are authorized to process and keep generated reports in an approved storage location. <br>
Risk: Fuzzy store-to-region matching can place unmatched or ambiguous stores in the wrong region or in Others. <br>
Mitigation: Review the store mapping CSV, aliases, and any stores assigned to Others before relying on the report. <br>
Risk: Missing, renamed, or mismatched weekly Excel files can produce incomplete or failed reports. <br>
Mitigation: Confirm all six current-week and six previous-week files are present and use the expected date and report naming patterns. <br>


## Reference(s): <br>
- [Store Mapping CSV](references/store_mapping.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Guidance] <br>
**Output Format:** [Excel workbook (.xlsx) with formatted summary tables and embedded charts, plus Python usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires 12 weekly input Excel files and a store mapping CSV; report accuracy depends on file naming, source spreadsheet structure, and mapping coverage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
