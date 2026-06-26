## Description: <br>
Skill 激活器 helps OpenClaw users discover automation opportunities, match them to existing skills, and generate fused skills for uncovered workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[love5209](https://clawhub.ai/user/love5209) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users, developers, and operators use this skill to scan their workspace for installed skills and profile or channel signals, identify underused skills and capability gaps, and recommend or generate automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local environment scans can expose workspace identity files, profile details, and configured-channel signals. <br>
Mitigation: Review SOUL.md, USER.md, IDENTITY.md, and scan output for secrets or private details before running or sharing results. <br>
Risk: Generated fused skills or glue scripts can introduce incorrect workflow logic or unsafe commands. <br>
Mitigation: Review generated SKILL.md files and scripts, then run an appropriate security scan before deployment. <br>


## Reference(s): <br>
- [Fusion Guide - Skill Activator](references/fusion-guide.md) <br>
- [Role Templates - Skill Activator](references/role-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/love5209/skill-activator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with generated SKILL.md content, optional shell commands, and optional script snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize local scan findings into recommendations; generated fused skills and scripts should be reviewed and scanned before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
