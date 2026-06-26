## Description: <br>
Complete Qlik Cloud analytics platform integration with 37 tools for health checks, search, app management, reloads, natural language queries, automations, AutoML, Qlik Answers AI, data alerts, spaces, users, licenses, data files, and lineage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[undsoul](https://clawhub.ai/user/undsoul) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, analysts, administrators, and developers use this skill to let an agent inspect and operate Qlik Cloud tenants, apps, reloads, automations, alerts, users, spaces, files, lineage, AutoML, and Qlik Answers. It is suited for business-data discovery, dashboard and app administration, operational monitoring, and natural-language analytics against Qlik Cloud data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's Qlik Cloud tenant through an API key. <br>
Mitigation: Use a least-privilege Qlik API key, keep credentials out of committed files and shared chats, and confirm QLIK_TENANT points to the intended HTTPS Qlik Cloud tenant. <br>
Risk: Some scripts can perform mutating or administrative actions, including delete, reload cancel, automation run, and alert trigger actions. <br>
Mitigation: Require human confirmation before running mutating scripts and review target app, reload, automation, or alert identifiers before execution. <br>


## Reference(s): <br>
- [Qlik Cloud skill on ClawHub](https://clawhub.ai/undsoul/qlik-cloud) <br>
- [Publisher profile](https://clawhub.ai/user/undsoul) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON responses from Qlik Cloud API scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts require QLIK_TENANT and QLIK_API_KEY and return JSON status, data, and timestamp fields.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
