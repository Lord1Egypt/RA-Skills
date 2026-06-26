## Description: <br>
Rules of the Claw installs a 56-rule OpenClaw Guardian baseline that blocks risky agent actions such as credential theft, data exfiltration, network scanning, and destructive infrastructure commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bahuleyandr](https://clawhub.ai/user/bahuleyandr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and customize a broad Guardian ruleset for OpenClaw environments. It is intended for teams that want deterministic tool-layer checks for secrets, outbound transfer, destructive commands, network scanning, and git remote changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer persistently replaces the local Guardian rules file with a broad blocking baseline, which may interrupt legitimate workflows if placeholders or noisy rules are left unchanged. <br>
Mitigation: Review the rule JSON before installation, keep the generated backup, replace app, organization, and user placeholders, and disable rules that are too restrictive for the target environment. <br>


## Reference(s): <br>
- [Rules of the Claw on ClawHub](https://clawhub.ai/bahuleyandr/rules-of-the-claw) <br>
- [OpenClaw Guardian plugin](https://github.com/fatcatMaoFei/openclaw-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs and validates Guardian rule configuration; users can edit placeholders and disable rules as needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
