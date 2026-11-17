## Description:

Security Operator provides runtime security guardrails for OpenClaw agents, covering prompt injection, excessive agency, cost runaway, credential leaks, cascade effects, setup guidance, and periodic audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevjade](https://clawhub.ai/user/kevjade)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to apply runtime guardrails, review community skills, audit credentials, and plan OpenClaw or VPS hardening before allowing persistent or high-risk changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional hardening script and credential audit create review-worthy risk if run without inspection.

Mitigation: Install only after review, and do not run the hardening script in apply mode until the shell injection issue is fixed and credential checks redact secret values.

Risk: The documented apply option does not match the script's implemented apply flag.

Mitigation: Confirm supported flags from artifact/scripts/install.sh before running any command that changes firewall state.

Risk: The setup flow can create persistent AGENTS.md changes and scheduled cron audits.

Mitigation: Treat AGENTS.md edits and cron setup as explicit opt-in changes that require review before enabling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevjade/skills/security-operator)
- [The Operator Vault](https://theoperatorvault.io)
- [Research Mode vs Execution Mode](artifact/references/modes-and-approval-gates.md)
- [Prompt Injection Guardrails](artifact/references/prompt-injection-guardrails.md)
- [VPS Hardening Checklist](artifact/references/vps-hardening-checklist.md)
- [Workshop Security Section](artifact/references/workshop-security-section.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes approval gates, audit checklists, and optional plan-only VPS hardening guidance.]

## Skill Version(s):

2.2.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
