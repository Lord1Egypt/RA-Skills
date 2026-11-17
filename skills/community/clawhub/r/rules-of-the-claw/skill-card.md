## Description:

Rules of the Claw installs deterministic OpenClaw Guardian rules intended to block credential theft, data exfiltration, network scanning, git poisoning, and destructive infrastructure operations at the tool layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bahuleyandr](https://clawhub.ai/user/bahuleyandr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and customize a baseline policy for OpenClaw Guardian that blocks high-risk agent file, shell, network, Docker, database, and git actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently replaces active OpenClaw Guardian rules with a broad policy.

Mitigation: Review rules-of-the-claw.json before installation and keep the installer's backup of the previous Guardian rules file.

Risk: Placeholders such as YOUR_ORG, YOUR_USER, and your_app may make rules too broad, too narrow, or operationally disruptive if left unchanged.

Mitigation: Customize placeholders for the target organization, user, application, Docker services, and database names before relying on the policy.

Risk: The ruleset is not complete protection against credential exfiltration or unsafe agent behavior.

Mitigation: Use it alongside sandboxing, network controls, file access restrictions, and normal review of sensitive agent actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bahuleyandr/skills/rules-of-the-claw)
- [OpenClaw Guardian plugin](https://github.com/fatcatMaoFei/openclaw-guardian)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [JSON configuration plus Markdown installation guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installer replaces the active OpenClaw Guardian rules file after creating a timestamped backup and requires Node.js v18+ for validation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
