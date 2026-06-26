## Description: <br>
Scans installed OpenClaw skills to detect missing authorization, configuration, or environment variables, and can disable or uninstall invalid skills on request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edde-101](https://clawhub.ai/user/edde-101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to audit installed skills, identify missing configuration or credentials, and clean up unusable skills after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The clean action can disable or forcibly uninstall installed skills. <br>
Mitigation: Run the report action first, verify every target skill name, and prefer disable before uninstall. <br>
Risk: Cleanup has weak built-in safeguards if an unintended skill name is supplied. <br>
Mitigation: Only run clean after explicitly choosing the exact skills to change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edde-101/skill2cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text diagnostic reports and cleanup logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-only mode lists skill status before any cleanup action.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
