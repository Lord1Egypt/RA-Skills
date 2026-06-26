## Description: <br>
OpenClaw security deployment guide to help users secure their OpenClaw installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jnMetaCode](https://clawhub.ai/user/jnMetaCode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review OpenClaw deployments for network exposure, container isolation, credential handling, audit logging, plugin security, and patch management. It returns prioritized security findings and concrete remediation commands for the user to review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security-audit checks may surface sensitive paths, environment details, or secret-adjacent findings in prompts or outputs. <br>
Mitigation: Use the skill only for intended local security audits, avoid sharing raw secret values, and review findings before copying or publishing output. <br>
Risk: Suggested hardening commands can change service exposure, file permissions, container privileges, or update behavior if applied without review. <br>
Mitigation: Confirm the target scope first and require user review before applying any remediation command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jnMetaCode/shellward-security-guide) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jnMetaCode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and security recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations should be reviewed before any command is executed, especially commands that change permissions, firewall rules, container settings, or update behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
