## Description: <br>
Convert manual incident runbooks into automated, executable playbooks. Parse existing runbooks, generate scripts for each step, add health checks, rollback procedures, and notification hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and on-call engineers use this skill to convert manual incident runbooks into executable playbooks, audit existing runbooks for automation gaps, dry-run generated playbooks, and create structured incident-response templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated playbooks can run operational commands that may affect production systems. <br>
Mitigation: Review generated scripts before running them, keep dry-run enabled during validation, and execute with least-privilege operational credentials. <br>
Risk: Optional Slack or PagerDuty notifications can send incident details to external destinations. <br>
Mitigation: Confirm notification destinations before use and avoid sending sensitive incident details to unapproved external channels. <br>
Risk: Generated automation may contain incorrect commands, stale assumptions, or misleading operational guidance. <br>
Mitigation: Validate commands, prerequisites, health checks, rollback steps, and escalation criteria against the source runbook before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash code blocks and generated shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated playbooks should be reviewed before execution and validated with dry-run mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
