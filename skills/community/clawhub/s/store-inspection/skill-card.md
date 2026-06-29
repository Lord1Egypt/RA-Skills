## Description: <br>
连锁门店巡店管理全流程助手，覆盖巡店计划制定、巡店执行评分、营销方案生成和数据分析报告四个阶段。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operations teams, regional managers, and store supervisors use this skill to plan inspections, score store execution across ten weighted dimensions, generate corrective actions, and summarize results in reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports load Chart.js from a third-party CDN, which may be unsuitable for sensitive or network-restricted inspection data. <br>
Mitigation: Avoid placing sensitive business data in generated reports when the CDN dependency is unacceptable, or review reports in an environment approved for that dependency. <br>
Risk: Inspection plans, scoring results, marketing plans, and reports are written as local files that may contain store operations details. <br>
Mitigation: Store and share generated files according to the organization's data handling rules, and review report contents before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/store-inspection) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with optional shell commands; the bundled script can write JSON data files and HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local script stores inspection plans, scoring results, marketing plans, and generated reports under its own data and output folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
