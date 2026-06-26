## Description: <br>
Skill Guardian monitors OpenClaw skill workspaces for new or changed skills, detects functional overlap, and maintains user-guide and README documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nathemkingh](https://clawhub.ai/user/nathemkingh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators and developers use the skill to monitor installed skill directories, identify new or changed skills, check for functional overlap, and keep user-facing guide files current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled operation can periodically read skill documentation across OpenClaw workspaces and update registry and guide files. <br>
Mitigation: Review the cron schedules, notification destination, and declared write scope before enabling scheduled scans. <br>
Risk: Generated overlap notices or user-guide updates may be incomplete or misleading if skill descriptions are ambiguous. <br>
Mitigation: Review generated overlap findings, guide files, and README changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nathemkingh/skill-lifecycle-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese text responses, Markdown guide files, JSON registry updates, and shell/cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update declared workspace files: memory/skill-registry.json, skills/user-guides/*.md, and skills/user-guides/README.md.] <br>

## Skill Version(s): <br>
2.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
