## Description: <br>
Scans installed skills, suggests L0-L3 priority tiers, and auto-configures skill injection policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to scan installed skills, assign priority tiers, and configure a token-aware skill injection policy for new setups, migrations, audits, or performance tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup messaging may overstate which local configuration files were changed. <br>
Mitigation: Verify AGENTS.md, SOUL.md, and message-injector configuration manually after running setup. <br>
Risk: Automatic setup can apply tiering choices before the user has reviewed the generated policy. <br>
Mitigation: Run with --dry-run first, review the proposed policy and tiers, and avoid --auto on first use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/halfmoon82/skill-priority-setup) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with shell commands and configuration file descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The setup flow can propose tier assignments, policy text, backups, validation output, and configuration changes for local review.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, clawhub.yaml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
