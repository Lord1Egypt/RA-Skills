## Description: <br>
Runtime security guardrails for OpenClaw agents that help manage prompt injection, excessive agency, cost runaway, credential leaks, cascade effects, setup, and periodic audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kevjade](https://clawhub.ai/user/Kevjade) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to add runtime guardrails, security audits, community skill vetting, and VPS hardening checks to OpenClaw agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional hardening installer can make persistent package and firewall changes when run with elevated privileges. <br>
Mitigation: Review the installer before use, run its plan-only mode first, and apply it only on a machine where firewall and package changes are expected. <br>
Risk: Untrusted SSH port or source values could lead to unsafe firewall configuration. <br>
Mitigation: Validate SSH inputs, confirm backup console access and rollback steps, and avoid privileged installer use until those values are trusted. <br>


## Reference(s): <br>
- [Security Operator on ClawHub](https://clawhub.ai/Kevjade/security-operator) <br>
- [The Operator Vault](https://theoperatorvault.io) <br>
- [Research Mode vs Execution Mode](references/modes-and-approval-gates.md) <br>
- [Prompt Injection Guardrails](references/prompt-injection-guardrails.md) <br>
- [VPS Hardening Checklist](references/vps-hardening-checklist.md) <br>
- [Workshop Security Section](references/workshop-security-section.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approval gates, audit summaries, guardrail text, and plan-only hardening commands.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
