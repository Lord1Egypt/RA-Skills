## Description: <br>
When the user uploads 发票.zip and 火车票.zip, use the included data tables to calculate eligible business-trip subsidy records, split related vs remaining files, create output workbooks, package two result zips, and report progress at every key step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AttorneyTao](https://clawhub.ai/user/AttorneyTao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and finance or operations staff use this skill to process invoice and train-ticket archives, calculate eligible business-trip subsidy records, separate excluded records, and package the resulting workbooks and files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded reimbursement archives may contain sensitive business-trip, invoice, route, lodging, and payment information. <br>
Mitigation: Use trusted archives, keep processing local, review generated subsidy calculations before submission, and delete the local run directory when the documents are sensitive. <br>
Risk: Ambiguous cities, dates, lodging evidence, or itinerary continuity can lead to incorrect subsidy eligibility. <br>
Mitigation: Prefer structured table data, exclude uncertain records from subsidy calculations, place unresolved records in the remaining set, and document the reason in the output workbook. <br>
Risk: Archive contents, filenames, and table values are untrusted inputs. <br>
Mitigation: Protect against zip slip and path traversal, never execute extracted files, and write only under the dedicated run directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AttorneyTao/travel-subsidy) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Progress messages plus generated workbooks and zip archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces subsidy and remaining-record zip packages from user-provided reimbursement archives; outputs should be reviewed before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
