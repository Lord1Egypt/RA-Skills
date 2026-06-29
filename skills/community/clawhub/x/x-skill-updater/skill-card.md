## Description: <br>
Checks installed OpenClaw skills for updates, reports available upgrades, and supports user-approved upgrades from configured SkillHub and ClawHub sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snlcc](https://clawhub.ai/user/snlcc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and workspace administrators use this skill to scan installed and workspace skills, compare local metadata with configured registries, review a generated update report, and run upgrades only after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The updater reads installed and workspace skill metadata and writes local report and source-tracking files. <br>
Mitigation: Use it only in OpenClaw environments where local skill metadata scanning and report generation are expected. <br>
Risk: Approved upgrades can replace installed skill code from configured external SkillHub or ClawHub sources. <br>
Mitigation: Review the generated report before approving upgrades, and be especially cautious with bulk upgrades. <br>
Risk: Incorrect source configuration can lead to checking or upgrading the wrong skill source. <br>
Mitigation: Keep skill-sources.json accurate and confirm unknown sources through the reply workflow before running upgrades. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snlcc/x-skill-updater) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/snlcc) <br>
- [SkillHub Registry Index](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/skills.json) <br>
- [ClawHub Skill API](https://clawhub.ai/api/skill?slug=) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local update reports and source-tracking JSON files; upgrade commands depend on configured external skill sources.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
