## Description: <br>
Generates a Chinese weekly report from configured Git repositories by grouping this week's commit history into functional modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anneheartrecord](https://clawhub.ai/user/anneheartrecord) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn configured repositories' weekly Git activity into a concise Chinese status report grouped by feature area. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads commit messages and changed-file paths from repositories listed in config.conf, which may expose private project details. <br>
Mitigation: Create and review config.conf yourself, include only intended repositories, and do not run the skill with a config file from an untrusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anneheartrecord/weekly-report-generator-by-git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown numbered list with indented subitems] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Git log output from repositories listed in config.conf and summarizes commit messages and changed-file paths in Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
