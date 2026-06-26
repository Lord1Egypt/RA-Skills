## Description: <br>
物流管理技能，提供提单生成、报关单据生成、物流跟踪等功能。支持 OKKI 客户数据同步和自动化文档处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Logistics and operations users can use this skill to create and manage logistics records, generate bills of lading and customs documents, track shipment status, send customer notifications, and optionally sync shipment follow-up records to OKKI CRM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated record, notification, CRM-sync, file, and subprocess capabilities could expose or alter logistics data if used as a public-facing API. <br>
Mitigation: Install only in a controlled local environment unless authentication and role checks are added. <br>
Risk: OKKI integration paths, subprocess execution, live sync during tests, and BOL file helpers require review before use. <br>
Mitigation: Constrain OKKI integration paths, pass a minimal environment to subprocesses, gate live sync during tests, and restrict BOL read/delete helpers to the archive directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-logistics-manager) <br>
- [End-to-end test report](artifact/test/e2e_test_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, and shell/CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local logistics records and document files; OKKI sync and notification behavior depend on environment configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
