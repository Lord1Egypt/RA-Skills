## Description: <br>
Checks whether an agent skill is suitable to install on the current machine by reviewing binaries, environment variables, configuration, OS, and sandbox conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill before installation to audit a skill directory and target environment, identify missing dependencies or configuration gaps, and produce reviewable installation and rollback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Python helper reads user-provided skill directories or input files and may write a report to a requested path. <br>
Mitigation: Run it only on intended skill materials, avoid broad sensitive folders, and review the generated report before making environment changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/skill-install-checker) <br>
- [README](artifact/README.md) <br>
- [Skill Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON report with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local report when an output path is provided; otherwise can return reviewable guidance directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
