## Description:

SecureClaw adds security rules and shell-based checks for OpenClaw agents covering auditing, credential protection, supply chain scanning, privacy checks, hardening, and incident response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adversa-ai](https://clawhub.ai/user/adversa-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators of OpenClaw, Moltbot, or Clawdbot agents use SecureClaw to audit local agent security, protect credentials and private details, scan skills for risky patterns, harden OpenClaw configuration, and respond to suspected compromise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SecureClaw installs persistent agent policy instructions and can modify OpenClaw guidance files.

Mitigation: Review the installer and hardening script before use, keep generated backups, and manually remove residual SecureClaw directives if uninstalling.

Risk: Broad audit and emergency workflows can reveal local paths, configuration state, process information, open ports, and recent file activity.

Mitigation: Run these workflows only in a trusted terminal and avoid sharing raw output externally.

Risk: Remote or unpinned command paths can add supply chain uncertainty when plugin commands or advisory feeds are used.

Mitigation: Prefer a verified local OpenClaw CLI and review remote package or feed sources before relying on them.

## Reference(s):

- [SecureClaw ClawHub release](https://clawhub.ai/adversa-ai/skills/secureclaw-skill)
- [Adversa AI](https://adversa.ai)
- [SecureClaw advisory feed](https://adversa-ai.github.io/secureclaw-advisories/feed.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and shell-script audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local audit, privacy check, skill scan, hardening, integrity check, advisory check, and emergency response workflows.]

## Skill Version(s):

2.2.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
