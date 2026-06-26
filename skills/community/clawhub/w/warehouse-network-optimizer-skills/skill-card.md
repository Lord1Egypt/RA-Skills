## Description: <br>
基于整数规划（MILP）的仓配网络优化系统，支持时效计算（含等待时间）、中转链路、供应关系到区县等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinqianfei](https://clawhub.ai/user/jinqianfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations analysts, logistics planners, and developers use this skill to convert warehouse, trunk-line, and distribution-cycle spreadsheets into optimization inputs, run MILP-based RDC network optimization, and generate Excel reports for warehouse selection, supply relationships, transfer paths, and weighted delivery-time metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON and Excel reports may expose sensitive business or logistics data. <br>
Mitigation: Run the skill only on spreadsheets intended for processing and protect generated files according to the user's data-handling requirements. <br>
Risk: Reports or converted data may overwrite existing files when output paths are reused. <br>
Mitigation: Use an empty working folder or explicit unique output filenames for each run. <br>
Risk: Large optimization datasets can consume significant solver time and local compute resources. <br>
Mitigation: Install dependencies in a virtual environment and test large runs with appropriate local resource limits. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/jinqianfei/warehouse-network-optimizer-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with command examples; generated JSON data and Excel reports when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local Excel and JSON logistics data, writes converted JSON files, and produces an .xlsx optimization report.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata and skill version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
