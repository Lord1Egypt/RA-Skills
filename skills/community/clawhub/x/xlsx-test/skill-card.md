## Description: <br>
Helps agents create, read, edit, fix, and convert spreadsheet files such as XLSX, XLSM, CSV, and TSV, with formula recalculation and validation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longxiangwang](https://clawhub.ai/user/longxiangwang) <br>

### License/Terms of Use: <br>
Proprietary. LICENSE.txt has complete terms <br>


## Use Case: <br>
Developers and spreadsheet-focused agents use this skill to inspect, create, repair, format, and recalculate spreadsheet deliverables. It is intended for workflows where the final deliverable is a spreadsheet file rather than a report, standalone script, database pipeline, or Google Sheets integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release as suspicious because it contains hidden or conflicting tool-governance text. <br>
Mitigation: Review the skill instructions before installation and disregard conflicting tool-selection claims unless they are confirmed by the platform owner. <br>
Risk: The security summary identifies out-of-scope Office document code beyond the spreadsheet workflow. <br>
Mitigation: Limit deployment to the intended spreadsheet use case and review any Word or PowerPoint processing paths before enabling them. <br>
Risk: The security guidance notes persistent LibreOffice macro behavior and possible native-code compilation and preloading. <br>
Mitigation: Run the skill in an isolated workspace and LibreOffice profile, and avoid processing sensitive original files without backups. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/longxiangwang/xlsx-test) <br>
- [Publisher profile](https://clawhub.ai/user/longxiangwang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; spreadsheet files may be created or modified by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The recalculation workflow returns JSON-style status and error summaries when formulas are checked.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
