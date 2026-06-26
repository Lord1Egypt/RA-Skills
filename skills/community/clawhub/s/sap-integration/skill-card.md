## Description: <br>
SAP system integration, data extraction, and automation for ABAP, HANA, and S/4HANA environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and SAP integration engineers use this skill to extract SAP data, call RFC/BAPI functions, generate ABAP and integration code, analyze SAP tables, automate workflows, and plan S/4HANA migration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad SAP read and RFC/BAPI execution capability. <br>
Mitigation: Use a dedicated least-privilege SAP account, prefer read-only roles, and restrict allowed RFC/BAPI functions and tables before deployment. <br>
Risk: Extracted JSON, CSV, or Excel outputs may expose sensitive business data. <br>
Mitigation: Treat exported data as sensitive, store it only in approved locations, and apply normal enterprise access controls and retention rules. <br>
Risk: The security verdict recommends caution before production use. <br>
Mitigation: Avoid production deployment until the skill has been reviewed and configured for the target SAP environment. <br>


## Reference(s): <br>
- [SAP HANA Integration Guide](artifact/references/hana-integration.md) <br>
- [S/4HANA Migration Guide](artifact/references/s4hana-migration.md) <br>
- [SAP Enhancement Framework Guide](artifact/references/enhancement-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with ABAP, Python, SQL, and shell code blocks; bundled scripts may produce JSON, CSV, or Excel data exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script outputs may contain sensitive SAP business data and should be handled under enterprise data controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
