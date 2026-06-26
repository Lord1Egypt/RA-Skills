## Description: <br>
Manage Linux applications by searching, installing, uninstalling, and updating software via Spark Store on Debian-based systems or APM across Linux distributions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vmomenv](https://clawhub.ai/user/vmomenv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Linux users and support agents use this skill to find applications, compare Spark Store and APM results, and prepare install, removal, or update commands for user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose sudo package-management commands that install, remove, or update Linux software. <br>
Mitigation: Before approval, show the exact aptss or apm command, package name, source, sudo requirement, and expected system impact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vmomenv/spark-store-skill) <br>
- [Spark Store categories API](https://d.spark-app.store/store/categories.json) <br>
- [APM categories API](https://d.spark-app.store/amd64-apm/categories.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands and package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sudo aptss or apm commands that should be shown to the user before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
