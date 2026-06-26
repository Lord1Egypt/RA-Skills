## Description: <br>
Skill Health Monitor helps agents and maintainers assess OpenClaw skill health with multidimensional scores, alert levels, and optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to check single skills or skill groups, review health scores and alert levels, and receive practical improvement recommendations before or after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad batch checks can lead an agent to inspect more skills than the user intended. <br>
Mitigation: Confirm the exact skill scope before running checks across multiple or all skills. <br>
Risk: Current health records and alerts are stored in memory and can be lost when the process restarts. <br>
Mitigation: Export or record important reports separately until a reviewed persistence feature is available. <br>
Risk: Health reports may recommend operational actions such as stopping service or rolling back a version. <br>
Mitigation: Require human approval before applying any service stop, rollback, notification, or automated remediation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/skill-health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown-style health reports and JavaScript object results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include skill name, health score, alert level, dimensional scores, recommendations, and timestamps.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
