## Description:

Generate Quantity Take-Off (QTO) reports from BIM/CAD data. Extract volumes, areas, counts by category. Group elements, apply calculation rules, and create cost estimates automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction estimators, BIM specialists, and project teams use this skill to summarize quantities from BIM/CAD exports, group elements by construction attributes, apply calculation rules, and prepare cost-estimation inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read user-provided BIM/CAD project data that contains confidential construction information.

Mitigation: Use only intended project files and confirm data-sharing permissions before processing.

Risk: Generated Excel, CSV, or JSON exports can overwrite existing files when generic names or reused output folders are selected.

Mitigation: Specify explicit filenames or dedicated output folders for generated reports.

Risk: Quantity and cost summaries depend on the accuracy of the source data, unit prices, and calculation rules supplied by the user.

Mitigation: Review source data, units, pricing assumptions, and formulas before using outputs for estimating or project decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/qto-report)
- [Data Driven Construction](https://datadrivenconstruction.io)
- [IfcOpenShell](https://ifcopenshell.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and prose with Python code snippets; optional Excel, CSV, and JSON report files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided CSV, Excel, JSON, BIM, or CAD-derived data and can create report exports in the working directory.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
