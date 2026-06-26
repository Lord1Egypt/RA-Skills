## Description: <br>
AI spreadsheet and Excel generation powered by CellCog for financial models, budget templates, data trackers, projections, pivot tables, complex formulas, XLSX output, analysis, charts, and professional formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to ask a CellCog agent to create spreadsheet workbooks, financial models, trackers, analysis templates, charts, formulas, and formatted XLSX or HTML spreadsheet tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet prompts and explicitly referenced files may be sent to CellCog and could include sensitive business, financial, personal, or proprietary data. <br>
Mitigation: Use only after approving CellCog's data handling for the intended data; redact or minimize sensitive inputs and avoid secrets, regulated personal data, and confidential records unless approved. <br>
Risk: The skill requires CELLCOG_API_KEY to access the external CellCog service. <br>
Mitigation: Store the API key in the agent environment or a secret manager; do not paste it into prompts or generated spreadsheets. <br>


## Reference(s): <br>
- [CellCog](https://cellcog.ai) <br>
- [ClawHub listing](https://clawhub.ai/nitishgargiitd/spreadsheets-cog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Files, Configuration] <br>
**Output Format:** [Markdown guidance with Python code snippets; generated spreadsheet files may be XLSX or interactive HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the cellcog package, and CELLCOG_API_KEY; sends spreadsheet prompts and referenced files to CellCog.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
