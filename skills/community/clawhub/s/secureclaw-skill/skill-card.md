## Description: <br>
SecureClaw is a security skill for OpenClaw agents that provides 15 core rules and automated scripts for auditing, credential protection, supply-chain scanning, privacy checking, hardening, and incident response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adversa-ai](https://clawhub.ai/user/adversa-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use SecureClaw to help OpenClaw agents audit local setups, check for privacy leaks, scan skills and supply-chain indicators, harden configuration, and respond to suspected compromise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist security rules into agent instruction files and change local OpenClaw configuration. <br>
Mitigation: Review install.sh and quick-harden.sh before running them, confirm the exact files they will edit, and keep backups of affected OpenClaw configuration and instruction files. <br>
Risk: Uninstalling may leave SecureClaw directives in local instruction files. <br>
Mitigation: After uninstalling, manually review AGENTS.md, TOOLS.md, SOUL.md, and related OpenClaw files and remove any SecureClaw directives that should no longer apply. <br>


## Reference(s): <br>
- [SecureClaw README](artifact/README.md) <br>
- [SecureClaw skill definition](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/adversa-ai/secureclaw-skill) <br>
- [Adversa AI](https://adversa.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with bash command examples and shell-script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local audit, hardening, privacy, integrity, supply-chain, advisory, and incident-response checks.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
