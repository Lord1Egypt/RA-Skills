## Description: <br>
Audits SAP FI/CO journal exports to flag duplicates, anomalies, unusual cost center use, approval bypass indicators, intercompany issues, and unusual user activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dda-oo](https://clawhub.ai/user/dda-oo) <br>

### License/Terms of Use: <br>
CC-BY-4.0 <br>


## Use Case: <br>
Controllers, internal auditors, finance teams, and audit-preparation teams use this skill for first-pass review of exported SAP FI/CO journal data. It produces categorized findings, management-ready recommendations, and machine-readable flagged entries for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SAP accounting exports can contain sensitive business data. <br>
Mitigation: Invoke the skill only for intended SAP FI/CO audit analysis and review generated memo and CSV files before sharing them. <br>
Risk: Flagged findings are indicators, not final audit conclusions. <br>
Mitigation: Require review by a controller, internal audit team, or other responsible finance professional before corrective action. <br>
Risk: The skill creates output files in the input file directory and stores limited run history. <br>
Mitigation: Run it in an approved workspace for accounting data and clean up generated files or retained history according to local data-handling policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dda-oo/sap-journal-auditor) <br>
- [SAP Journal Auditor README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Security Policy](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, Files, Guidance] <br>
**Output Format:** [Markdown audit memo, flagged-entry CSV, and concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English or German output; creates audit_memo.md and flagged_entries.csv in the input file directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
