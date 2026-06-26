## Description: <br>
Enforces skill-trust-scanner security checks before installing ClawHub skills, blocking or warning based on risk scores to reduce supply chain threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Walkman1W](https://clawhub.ai/user/Walkman1W) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to add a security gate before ClawHub skill installation. It scans local, Git, or registry-sourced skills and applies allow, warn, or reject decisions before installation proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper depends on a separate local scanner that is not bundled with this release. <br>
Mitigation: Pin and review the scanner installation path before relying on guard decisions. <br>
Risk: The PATH shim can intercept future `clawhub install` commands. <br>
Mitigation: Prefer explicit `install.sh` use until the shim path, uninstall process, and revert steps have been reviewed. <br>
Risk: `--yes` can auto-approve warning-range skills. <br>
Mitigation: Review scanner output before using `--yes` for skills that receive a warning decision. <br>


## Reference(s): <br>
- [Skill Trust Guard ClawHub page](https://clawhub.ai/Walkman1W/skill-trust-guard) <br>
- [Walkman1W publisher profile](https://clawhub.ai/user/Walkman1W) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes security scan decisions such as allow, warn, or reject, plus installation and PATH configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
