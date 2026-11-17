## Description:

基于整数规划（MILP）的仓配网络优化系统，支持时效计算（含等待时间）、中转链路、供应关系到区县等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqianfei](https://clawhub.ai/user/jinqianfei)

### License/Terms of Use:

MIT-0

## Use Case:

External logistics planners, operations teams, and developers use this skill to convert warehouse trunk-line and distribution-cycle spreadsheets into JSON, configure RDC constraints, and run MILP warehouse network optimization. It produces local reports for RDC selection, supply relationships, transfer paths, regional assignment, and weighted delivery-time analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization reports can be misleading if source logistics workbooks, bundled JSON data, or planning assumptions are incorrect.

Mitigation: Validate source workbooks and converted JSON, confirm RDC count plus required or forbidden warehouse constraints, and review outputs before making warehouse or financial decisions.

Risk: Local workbook processing and generated Excel files can carry file-handling and dependency risks when inputs come from others.

Mitigation: Run the scripts in an isolated virtual environment, pin dependencies for production use, and treat generated Excel reports as untrusted until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinqianfei/skills/warehouse-network-optimizer-skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with bash and Python examples; local JSON conversion outputs and Excel optimization reports from the included scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Excel inputs and Python dependencies including PuLP, pandas, and openpyxl.]

## Skill Version(s):

2.7.0 (source: server release metadata and SKILL.md status)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
