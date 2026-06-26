## Description: <br>
Validates Stylelint configuration files for errors, deprecated rules, config structure, plugins, extends, and overrides, returning text, summary, or JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to inspect Stylelint configuration files before local development, CI enforcement, or Stylelint 16 migration work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code and reads the configuration file path provided by the user. <br>
Mitigation: Run it only on intended project Stylelint configuration files and review the results before changing project lint configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/stylelint-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, one-line summary, or structured JSON from local command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish pass, validation failure, and file or parse errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
