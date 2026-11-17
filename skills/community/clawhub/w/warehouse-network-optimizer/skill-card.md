## Description:

基于整数规划（MILP）的仓配网络优化系统，支持时效计算（含等待时间）、中转链路、供应关系到区县等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinqianfei](https://clawhub.ai/user/jinqianfei)

### License/Terms of Use:

MIT-0

## Use Case:

Logistics planners and operations engineers use this skill to convert warehouse network data, configure RDC limits, and run MILP-based warehouse distribution optimization. It helps compare selected RDCs, supply relationships, transit links, province assignments, and weighted delivery timing in generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Excel or JSON inputs could affect local optimization results or generated reports.

Mitigation: Run the skill in a normal project or virtual environment and use only trusted or reviewed Excel and JSON inputs.

Risk: Generated .xlsx reports may preserve formula-like values from supplied data.

Mitigation: Review generated spreadsheets before opening or sharing reports created from third-party data.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with bash and Python examples, plus generated JSON and Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local optimization artifacts, including converted trunk-line and distribution-cycle JSON data and Excel reports with summary, RDC selection, supply relationships, transfer links, and province distribution sheets.]

## Skill Version(s):

2.7.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
