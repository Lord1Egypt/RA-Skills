## Description: <br>
Generate Quantity Take-Off (QTO) reports from BIM/CAD data by extracting volumes, areas, and counts, grouping elements, applying calculation rules, and creating cost estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction teams, estimators, and BIM/CAD practitioners use this skill to turn user-provided project data into structured QTO summaries, material breakdowns, and cost-estimate inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QTO quantities and cost estimates may be incorrect or incomplete if source BIM/CAD data, unit prices, rules, or units are wrong. <br>
Mitigation: Validate inputs, review generated quantities and cost estimates before business use, and reconcile outputs against project standards. <br>
Risk: The skill reads user-provided project files and can write reports to output locations. <br>
Mitigation: Provide only intended project files, choose explicit output locations, and avoid processing sensitive files that are outside the reporting task. <br>
Risk: The server release version and artifact configuration version differ. <br>
Mitigation: Use the server release version for this card and verify the artifact version if exact provenance or release matching is required. <br>


## Reference(s): <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [IfcOpenShell](https://ifcopenshell.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with structured tables and optional Excel, CSV, or JSON export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided BIM/CAD data and report parameters; supports CSV, Excel, JSON, IFC-derived data, and direct input patterns described in the artifact.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact claw.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
