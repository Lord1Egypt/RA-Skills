## Description: <br>
Validates JSON-exported webpack configuration files for structural issues, deprecated loaders/plugins, optimization gaps, and best-practice concerns when auditing configs, preparing production builds, or enforcing CI standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and build/release engineers use this skill to validate JSON-exported webpack configs, identify structural, deprecation, and optimization issues, and generate checks or fix suggestions for local audits or CI standards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exporting a webpack config with Node executes code from the target project. <br>
Mitigation: Use trusted repositories or a disposable environment before exporting configs from untrusted projects. <br>
Risk: The validator works on JSON-exported webpack configs and cannot directly parse raw JS or TS config files. <br>
Mitigation: Export the config to JSON first and review non-serializable functions or regular expressions that may lose detail during export. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/webpack-config-validator) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Release status](artifact/STATUS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; validator output can be text, JSON, or summary format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports validate, check, explain, and suggest modes; strict mode can fail CI when warnings are present.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
