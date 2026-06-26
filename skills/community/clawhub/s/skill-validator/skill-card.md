## Description: <br>
A ClawHub skill-format validator that checks required files, package metadata, shell script syntax, permissions, and release-readiness issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub publishers use this skill to validate skill package structure before release, including SKILL.md, package.json, shell scripts, permissions, and configuration fields. It helps identify format and compatibility problems and can emit human-readable or JSON validation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation points users toward a curl-downloaded publishing adapter that is not part of the packaged artifact. <br>
Mitigation: Use the packaged validator scripts for validation tasks, and inspect any externally downloaded adapter before running it. <br>
Risk: Some documented workflows perform publishing or bulk publishing actions that can affect ClawHub, GitHub, local files, and account state. <br>
Mitigation: Run publishing commands only after reviewing target paths, account configuration, release metadata, and generated packages. <br>
Risk: The installer writes local configuration, rule, log, and example files under the user's OpenClaw configuration directory. <br>
Mitigation: Review installation effects before running install.sh, especially on shared or managed systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/skill-validator) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Skill development guide](https://github.com/openclaw/openclaw/docs/skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON validation report with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local validator configuration, rule files, logs, and example skill files under the user's OpenClaw configuration directory during installation.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
